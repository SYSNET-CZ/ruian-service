# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         query
# Purpose:      Querying the database
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
from typing import List, Any

import psycopg2
# from psycopg2._psycopg import cursor

from service.database import execute_sql, number_to_string, none_to_string, number_value, \
    PostGisDatabase, format_to_query, DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, commit_sql, \
    get_ruian_version
from service.models import Address

__author__ = 'SYSNET'

ITEM_TO_FIELD = {
    "id": "gid",
    "street": "nazev_ulice",
    "house_number": "cislo_domovni",
    "record_number": "cislo_domovni",
    "orientation_number": "cislo_orientacni",
    "orientation_number_character": "znak_cisla_orientacniho",
    "zip_code": "psc",
    "locality": "nazev_obce",
    "locality_part": "nazev_casti_obce",
    "district_number": "nazev_mop",
    "x": "latitude",
    "y": "longitude"
}

ADDRESSPOINTS_TABLE_NAME = "address_points"
ADDRESSPOINTS_COLUMNS_FIND = "nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, " \
                             "nazev_obce, nazev_casti_obce, nazev_mop "
ADDRESSPOINTS_COLUMNS_NEARBY = "gid, nazev_obce, nazev_casti_obce, nazev_ulice, typ_so, cislo_domovni, " \
                               "cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop"
ADDRESSPOINTS_COLUMNS_VALIDATE = "gid, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, " \
                                 "nazev_casti_obce, nazev_mop, nazev_ulice, typ_so"

ADDRESSPOINTS_COLUMNS_FIND_COORD = "latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, " \
                                   "cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop"

MAX_COUNT = 10


def _find_address(identifier):
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_FIND + \
          " FROM " + ADDRESSPOINTS_TABLE_NAME + \
          " WHERE gid = " + str(identifier)
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    if row:
        (house_number, record_number) = analyse_row(row[2], number_to_string(row[1]))
        a = number_value(none_to_string(row[8]))
        address = Address(none_to_string(row[0]), house_number, record_number,
                          number_to_string(row[3]), none_to_string(row[4]), number_to_string(row[5]),
                          none_to_string(row[6]), none_to_string(row[7]), a)
        return address
    else:
        return None


def _get_nearby_localities(y, x, distance, max_count=MAX_COUNT):
    max_count = int(max_count)
    if max_count > 10000:
        max_count = 10000
    geom = "the_geom,ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_NEARBY + \
          ", ST_Distance(%s) d1 FROM %s WHERE ST_DWithin(%s,%s) order by d1 LIMIT %s;" \
          % (geom, ADDRESSPOINTS_TABLE_NAME, geom, str(distance), str(max_count))
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    rows = cur.fetchall()
    return rows


def _validate_address(dictionary, return_row=False):
    first = True
    one_house_number = False
    db = PostGisDatabase(DATABASE_NAME_RUIAN)
    cur = db.get_cursor()

    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_VALIDATE + " FROM " + ADDRESSPOINTS_TABLE_NAME + " WHERE "
    work_tuple = ()
    for key in dictionary:
        if key == "house_number":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                sql += add_to_query("typ_so", "=", first)
                first = False
                work_tuple = work_tuple + (u"č.p.",)
            else:
                continue
        if key == "record_number":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                sql += add_to_query("typ_so", "=", first)
                first = False
                work_tuple = work_tuple + (u"č.ev.",)
            else:
                continue

        if key == "district_number" and dictionary[key] != "":
            value = format_to_query(dictionary["locality"] + " " + dictionary["district_number"])
        else:
            value = format_to_query(dictionary[key])
        work_tuple = work_tuple + (value,)

        if value is None:
            comparator = "is"
        else:
            comparator = "="
        sql += add_to_query(ITEM_TO_FIELD[key], comparator, first)
        first = False

    a = cur.mogrify(sql, work_tuple)
    cur.execute(a)
    row = cur.fetchone()

    result = None
    if return_row:
        if row:
            result = row
    else:
        if row:
            result = ["True"]
        else:
            result = ["False"]
    return result


def _find_coordinates(identifier):
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_FIND_COORD + \
          " FROM " + ADDRESSPOINTS_TABLE_NAME + \
          " WHERE gid = " + str(identifier)
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    if row and row[0] is not None and row[1] is not None:
        (house_number, record_number) = analyse_row(row[7], number_to_string(row[6]))
        c = (
            str("{:10.2f}".format(row[1])).strip(), str("{:10.2f}".format(row[0])).strip(),
            row[2], row[3], none_to_string(row[4]), none_to_string(row[5]),
            house_number, record_number, number_to_string(row[8]), none_to_string(row[9]),
            number_to_string(row[10]), number_value(none_to_string(row[11]))
        )
        return [c]
    else:
        return []


def _find_coordinates_by_address(dictionary):
    if "district_number" in dictionary:
        if dictionary["district_number"] != "":
            dictionary["district_number"] = "Praha " + dictionary["district_number"]

    first = True
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_FIND_COORD + \
          " FROM " + ADDRESSPOINTS_TABLE_NAME + \
          " WHERE "
    for key in dictionary:
        if dictionary[key] != "":
            if first:
                sql += ITEM_TO_FIELD[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                sql += " AND " + ITEM_TO_FIELD[key] + " = '" + dictionary[key] + "'"

    sql += "LIMIT " + str(MAX_COUNT)
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    rows = cur.fetchall()
    coordinates = []

    for row in rows:
        if (row[0] is not None) and (row[1] is not None):
            (house_number, record_number) = analyse_row(row[7], number_to_string(row[6]))
            coordinates.append(
                (str("{:10.2f}".format(row[0])).strip(), str("{:10.2f}".format(row[1])).strip(),
                 row[2], row[3], none_to_string(row[4]), none_to_string(row[5]),
                 house_number, record_number, number_to_string(row[8]), none_to_string(row[9]),
                 number_to_string(row[10]), number_value(none_to_string(row[11])))
            )
        else:
            # co se ma stat kdyz adresa nema souradnice?
            pass
    return coordinates


def _get_ruian_version_date():
    return get_ruian_version()


def _set_ruian_version_data_today():
    try:
        sql = 'DROP TABLE IF EXISTS ruian_dates;'
        sql += 'CREATE TABLE ruian_dates (id serial PRIMARY KEY, validfor varchar);'
        import time
        value = time.strftime("%d.%m.20%y")
        sql += "INSERT INTO ruian_dates (validfor) VALUES ('%s')" % value
        commit_sql(DATABASE_NAME_RUIAN, sql)
    except psycopg2.Error as e:
        result = "Error: Could connect to %s at %s:%s as %s\n%s" \
                 % (DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, str(e))
        print(result)
    pass


def get_table_count(table_name):
    cur = None
    try:
        sql = "SELECT count(*) FROM %s;" % table_name
        cur = execute_sql(DATABASE_NAME_RUIAN, sql)
        row = cur.fetchone()
        result = row[0]

    finally:
        cur.close()

    return str(result)


def _get_database_details():
    return None


def _get_table_names():
    return None


def _get_addresses(query_params):
    sql_items = {
        "house_number": "cast(cislo_domovni as text) like '%s%%' and typ_so='č.p.'",
        "record_number": "cast(cislo_domovni as text) ilike '%s%%' and typ_so<>'č.p.'",
        "orientation_number": "cast(cislo_orientacni as text) like '%s%%'",
        "orientation_number_character": "znak_cisla_orientacniho = '%s'",
        "zip_code": "cast(psc as text) like '%s%%'",
        "locality": "nazev_obce ilike '%%%s%%'",
        "street": "nazev_ulice ilike '%%%s%%'",
        "locality_part": "nazev_casti_obce ilike '%%%s%%'",
        "district_number": "nazev_mop = 'Praha %s'"
    }

    fields = " cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, " \
             "nazev_mop, nazev_ulice, typ_so, gid "

    sql_parts = []
    for key in sql_items:
        dict_key = key[:1].lower() + key[1:]
        if dict_key in query_params:
            if query_params[dict_key] != "":
                sql_parts.append(sql_items[key] % (query_params[dict_key]))

    if len(sql_parts) == 0:
        return []

    sql_base = u" from %s where " % ADDRESSPOINTS_TABLE_NAME + " and ".join(sql_parts)

    search_sql = u"select %s %s order by nazev_obce, nazev_casti_obce, psc, nazev_ulice, nazev_mop, " \
                 u"typ_so, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho limit 2" % (fields, sql_base)
    rows = execute_sql(DATABASE_NAME_RUIAN, search_sql)

    result: List[Any] = []
    for row in rows:
        result.append(row)

    return result


def analyse_row(typ_so, cislo_domovni):
    # Analyses typ_so value and sets either house_number or record_number to cislo_domovni.
    house_number = cislo_domovni
    record_number = 0
    try:
        if typ_so[-3:] == ".p.":
            house_number = number_to_string(cislo_domovni)
            record_number = ""
        elif typ_so[-3:] == "ev.":
            house_number = ""
            record_number = number_to_string(cislo_domovni)
        else:
            pass
    finally:
        return house_number, record_number


def add_to_query(attribute, comparator, first):
    if first:
        query = attribute + " " + comparator + " %s"
    else:
        query = " AND " + attribute + " " + comparator + " %s"
    return query
