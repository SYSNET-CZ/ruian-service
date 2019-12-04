# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         database
# Purpose:      Communication with PostGIS database
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------

import os
import sys
from datetime import datetime
import psycopg2
from postgis.psycopg import register

# from postgis import LineString
# from postgis import Point

__author__ = 'SYSNET'

DATABASE_HOST = os.getenv("POSTGIS_HOST", "postgis")
DATABASE_PORT = os.getenv("POSTGIS_PORT", 5432)
DATABASE_NAME_RUIAN = os.getenv("RUIAN_DATABASE", "ruian")
DATABASE_NAME_POVODI = os.getenv("POVODI_DATABASE", "povodi")
DATABASE_NAME_MAPY = os.getenv("MAPY_DATABASE", "mapy")
DATABASE_USER = os.getenv("POSTGIS_USER", "docker")
DATABASE_PASS = os.getenv("POSTGIS_PASSWORD", "docker")

ADMINISTRATIVE_DIVISION_TABLE_NAME = "administrative_division"
ADMINISTRATIVE_DIVISION_ZSJ_TABLE_NAME = "administrative_division_zsj"
ADMINISTRATIVE_DIVISION_KU_TABLE_NAME = "administrative_division_ku"
ADDRESSPOINTS_TABLE_NAME = "address_points"
FULLTEXT_TABLENAME = "fulltext"
ZVM50KLAD_TABLENAME = "zvm50klad"

TOWNNAME_FIELDNAME = "nazev_obce"
STREETNAME_FIELDNAME = "nazev_ulice"
TOWNPART_FIELDNAME = "nazev_casti_obce"
GID_FIELDNAME = "gid"
GIDS_FIELDNAME = "gids"
TYP_SO_FIELDNAME = "typ_so"
CISLO_DOMOVNI_FIELDNAME = "cislo_domovni"
CISLO_ORIENTACNI_FIELDNAME = "cislo_orientacni"
ZNAK_CISLA_ORIENTACNIHO_FIELDNAME = "znak_cisla_orientacniho"
ZIP_CODE_FIELDNAME = "psc"
MOP_NUMBER = "nazev_mop"
MOP_NAME = "nazev_mop"


def format_to_query(item):
    if item == "":
        return None
    elif item.strip().isdigit():
        return int(item)
    else:
        return item


def number_value(number_string):
    if number_string != "":
        s = number_string.split(" ")
        return s[1]
    else:
        return ""


class PostGisDatabase(object):

    def __init__(self, db_name):
        try:
            if db_name is None:
                db_name = DATABASE_NAME_RUIAN

            self.connection = psycopg2.connect(host=DATABASE_HOST, database=db_name,
                                               port=DATABASE_PORT, user=DATABASE_USER,
                                               password=DATABASE_PASS)
            register(self.connection)
            # self.cursor = None
            # print('PostGisDatabase created.')
        except psycopg2.Error as e:
            result = "Error: Could not connect to database %s at %s:%s as %s" % (
                DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER)
            # logger.info("Error: " + e.pgerror)
            print(str(result) + "\n" + str(e.pgerror))

    def get_cursor(self):
        cur = self.connection.cursor()
        return cur

    def get_query_result(self, query):
        cur = None
        rows = []
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            row_count = 0
            for row in cur:
                row_count += 1
                rows.append(row)

        except psycopg2.Error as e:
            result = "Error: Could not execute query to %s at %s:%s as %s:%s" % (
                DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, query)
            # logger.info("Error: " + e.pgerror)
            print(result + "\n" + e.pgerror)

        finally:
            cur.close()
            return rows

    def get_info(self):
        par = self.connection.get_dsn_parameters()
        print(par, "\n")
        return par


def get_ruian_version():
    cur = None
    sql = 'SELECT * FROM ruian_dates'
    try:
        db = PostGisDatabase(DATABASE_NAME_RUIAN)
        cur = db.connection.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        result = row[1]
        return result
    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s\n%s" \
                 % (DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql, str(e))
        return result
    finally:
        cur.close()


def get_rows(db_name, sql):
    out = []
    try:
        cur = execute_sql(db_name, sql)
        rows = cur.fetchall()
        cur.close()
        row_count = 0
        for row in rows:
            row_count += 1
            out.append(row[0])
        return out
    except (ValueError, Exception) as e:
        print(e)
        return out


def get_row(db_name, sql):
    out = None
    try:
        cur = execute_sql(db_name, sql)
        out = cur.fetchone()
        cur.close()
        return out
    except (ValueError, Exception) as e:
        print(e.pgerror)
        return out


def get_result(db_name, sql):
    if sql is None or sql == "":
        return None
    try:
        db = PostGisDatabase(db_name)
        rows = db.get_query_result(sql)
        return rows
    except psycopg2.Error as e:
        result = "Error: Could not get result for %s at %s:%s as %s:%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql)
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return []


def execute_sql(db_name, sql):
    if sql is None or sql == "":
        return None

    try:
        db = PostGisDatabase(db_name)
        cur = db.connection.cursor()
        cur.execute(sql)
        return cur

    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql)
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return None

    except (ValueError, Exception):
        return [sys.exc_info()[0]]


def commit_sql(db_name, sql):
    if sql is None or sql == "":
        return False

    try:
        db = PostGisDatabase(db_name)
        cur = db.connection.cursor()
        cur.execute(sql)
        db.connection.commit()
        cur.close()
        return True

    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s\n/%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql, str(e))
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return False

    except (ValueError, Exception):
        print([sys.exc_info()[0]])
        return False


def get_table_size(db_name, table_name):
    sql = "SELECT count(*) FROM " + table_name

    try:
        db = PostGisDatabase(db_name)
        out = db.get_query_result(sql)
        return out[0][0]

    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s\n/%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql, str(e))
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return -1

    except (ValueError, Exception):
        print([sys.exc_info()[0]])
        return -1


def get_tables(db_name):
    sql = "select table_schema, table_name, (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count from ( " \
          "select table_name, table_schema, query_to_xml(format('select count(*) as cnt from %I.%I', table_schema, " \
          "table_name), false, true, '') as xml_count from information_schema.tables where table_schema = 'public' ) t "

    try:
        db = PostGisDatabase(db_name)
        out = db.get_query_result(sql)
        return out

    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s\n/%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql, str(e))
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return False

    except (ValueError, Exception):
        print([sys.exc_info()[0]])
        return False


def get_table_names(db_name):
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"
    try:
        db = PostGisDatabase(db_name)
        nam = db.get_query_result(sql)
        out = []
        for n in nam:
            out.append(n[0])
        return out

    except psycopg2.Error as e:
        result = "Error: Could not execute query to %s at %s:%s as %s:%s\n/%s" % (
            DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, sql, str(e))
        # logger.info("Error: " + e.pgerror)
        print(result + "\n" + e.pgerror)
        return False

    except (ValueError, Exception):
        print([sys.exc_info()[0]])
        return False


def db_info(db_name):
    try:
        db = PostGisDatabase(db_name)
        return db.get_info()

    except (ValueError, Exception):
        return [sys.exc_info()[0]]


def get_obec_by_name(name):
    sql = "SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(
        TOWNNAME_FIELDNAME, "ac_obce", name)
    return get_rows(DATABASE_NAME_RUIAN, sql)


def get_ulice_by_name(name):
    sql = "SELECT {0} FROM {1} WHERE {0} ILIKE '%{2}%' GROUP BY {0} LIMIT 25".format(
        STREETNAME_FIELDNAME, "ac_ulice", name)
    return get_rows(DATABASE_NAME_RUIAN, sql)


def get_cast_obce_by_name(name):
    sql = "SELECT nazev_casti_obce FROM ac_casti_obce WHERE nazev_casti_obce ilike '%" + \
          name + "%' group by nazev_casti_obce limit 25"
    return get_rows(DATABASE_NAME_RUIAN, sql)


class DatabaseError(Exception):

    def __init__(self, message):
        Exception.__init__(message)

        self.when = datetime.now()
