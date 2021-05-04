# -*- coding: utf-8 -*-

from service.models import _SearchItem, none_to_string
from service.query import TOWNNAME_FIELDNAME, STREETNAME_FIELDNAME, \
    TOWNPART_FIELDNAME, MAX_TEXT_COUNT, \
    compile_address

__author__ = 'Radim Jäger'


def old_get_combined_text_searches(items):
    sql_list = []
    sql_sub_list = []

    def add_combination(sql_condition):
        # global sql_sub_list
        if not sql_sub_list:
            sql_sub_list.append(sql_condition)
        else:
            for i in range(len(sql_sub_list)):
                sql_sub_list[i] += " and " + sql_condition

    def add_candidates(field_name, value_list):
        if value_list is not None and value_list != []:
            for it in value_list:
                add_combination(field_name + " = '" + it + "'")

    for item in items:
        if item.isTextField():
            sql_sub_list = []
            add_candidates(TOWNNAME_FIELDNAME, item.towns)
            add_candidates(TOWNPART_FIELDNAME, item.townParts)
            add_candidates(STREETNAME_FIELDNAME, item.streets)

            if not sql_list:
                sql_list.extend(sql_sub_list)
            else:
                new_list = []
                for oldItem in sql_list:
                    for newItem in sql_sub_list:
                        new_list.append(oldItem + " and " + newItem)
                sql_list = []
                sql_list.extend(new_list)
    return sql_list


def get_text_items(items):
    result = []
    for item in items:
        if item.isTextField():
            result.append(item)
        if len(result) == MAX_TEXT_COUNT:
            break
    return result


def get_text_variants(text_items):
    streets = []
    towns = []
    town_parts = expanded_text_items(text_items)
    if not streets:
        streets = [_SearchItem(None, None, None)]
    if not towns:
        towns = [_SearchItem(None, None, None)]
    if not town_parts:
        town_parts = [_SearchItem(None, None, None)]
    return streets, towns, town_parts


def expanded_text_items(search_items):
    result = []
    for item in search_items:
        for street in item.streets:
            result.append(_SearchItem(item, street, STREETNAME_FIELDNAME))

        for town in item.towns:
            result.append(_SearchItem(item, town, TOWNNAME_FIELDNAME))

        for townPart in item.townParts:
            result.append(_SearchItem(item, townPart, TOWNPART_FIELDNAME))

    return result


def get_combined_text_searches(items):
    text_items = get_text_items(items)
    sql_items = []
    for item in text_items:
        sql_items.append(item)
    return []


def add_id(identifier, value, string, builder):
    if builder.formatText == "json":
        return '\t"%s": %s,\n%s' % (identifier, value, string)
    elif builder.formatText == "xml":
        return '\t<%s>%s</%s>\n%s' % (identifier, value, identifier, string)
    else:
        return value + builder.lineSeparator + string


def build_address(builder, candidates, with_id, with_distance=False):
    items = []
    for item in candidates:
        if item[4] == "č.p.":
            house_number = str(item[5])
            record_number = ""
        else:
            house_number = ""
            record_number = str(item[5])

        mop = none_to_string(item[9])
        if mop != "":
            pom = mop.split()
            district_number = pom[1]
        else:
            district_number = ""

        # TODO compiled address
        sub_str = compile_address(
            text_format=builder,
            street=none_to_string(item[3]),
            house_number=house_number,
            record_number=record_number,
            orientation_number=none_to_string(item[6]),
            orientation_number_character=none_to_string(item[7]),
            zip_code=str(item[8]),
            locality=none_to_string(item[1]),
            locality_part=none_to_string(item[2]),
            district_number=district_number,
            district_name=mop
        )

        if with_id:
            sub_str = add_id("id", str(item[0]), sub_str, builder)
        if with_distance:
            sub_str = add_id("distance", str(item[10]), sub_str, builder)
        items.append(sub_str)
    return items
