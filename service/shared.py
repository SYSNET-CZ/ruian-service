# -*- coding: utf-8 -*-
# NOT USED
# -------------------------------------------------------------------------------
# Name:        shared
# Purpose:
#
# Author:      Radim Jäger
# Copyright:   (c) SYSNET s.r.o.  2019
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

from urllib import parse

from common import TEXT_FORMAT_XML, TEXT_FORMAT_HTML, TEXT_FORMAT_HTML2ONEROW, TEXT_FORMAT_JSON, \
    TEXT_FORMAT_TEXT2ONEROW, LINE_SEPARATOR_HTML
from models import none_to_string

services = []


def get_result_format_param():
    return RestParam("/Format", u"Formát", u"Formát výsledku služby (HTML, XML, Text, JSON)")


def get_search_text_param():
    return URLParam("SearchText", u"Adresa", u"Adresa ve tvaru ulice číslo, část obce, "
                                             u"obec, PSČ", html_tags=' class="RUIAN_TEXTSEARCH_INPUT" required ')


def get_address_place_id_param_rest():
    return RestParam("/AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")


def get_zip_code_url(disabled=True):
    # psc = 10000...79862
    return URLParam("zip_code", u"PSČ", u"Poštovní směrovací číslo v rozsahu 100000 až 79862", "", disabled,
                    html_tags=' class="RUIAN_ZIP_INPUT" onkeypress="return isNumber(event, this, 5, 79862)" ')
    # onpaste="return isNumber(event, this, 5, 79862)"')


def get_house_number_url(disabled=True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return URLParam("house_number", u"Číslo popisné", "Číslo popisné v rozsahu 1 až 9999", "", disabled,
                    html_tags=' class="RUIAN_house_number_INPUT" onkeypress="return isNumber(event, this, 4, 0)" ')
    # onpaste="return isNumber(event, this, 4, 0)"')


def get_record_number_url(disabled=True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return URLParam("record_number", u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno, v rozsahu 1 až 9999",
                    "", disabled,
                    html_tags=' class="RUIAN_record_number_INPUT"  onkeypress="return isNumber(event, this, 4, 0)" ')
    # onpaste="return isNumber(event, this, 4, 0)"')


def get_orientation_number_url(disabled=True):
    # cislo_orientacni = 1..999
    return URLParam("orientation_number", u"Číslo orientační", "Číslo orientační v rozsahu 1 až 999", "", disabled,
                    html_tags=' class="RUIAN_orientation_number_INPUT" onkeypress="return isNumber(event, this, 3, 0)" ')
    # onpaste="return isNumber(event, this, 3, 0)"')


def get_orientation_number_character_url(disabled=True):
    # Písmeno čísla orientačního a..z, A..Z
    return URLParam("orientation_number_character",
                    u"Písmeno čísla<br>orientačního", "Písmeno čísla orientačního a..z, A..Z", "", disabled,
                    html_tags=' class="RUIAN_orientation_number_character_INPUT" onkeypress="return isENLetter(event, this)" ')


def get_district_number_url(disabled=True):
    # 1..10
    return URLParam("district_number", u"Městský obvod", u"Číslo městského obvodu v Praze", "", disabled,
                    html_tags=' class="RUIAN_district_number_INPUT" onkeypress="return isNumber(event, this, 2, 10)" ')
    # onpaste="return isNumber(event, this, 2, 10)"')


def get_address_place_id_param_url():
    # gid = 19..72628626
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa, maximálně 8 číslic", "", True,
                    html_tags=' class="RUIAN_ID_INPUT" onkeypress="return isNumber(event, this, 8, 0)" required ')


def get_address_place_id_param_url_id_not_disabled():
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa, maximálně 8 číslic", "", False,
                    html_tags=' class="RUIAN_ID_INPUT" onkeypress="return isNumber(event, this, 8, 0)" required ')


class HTTPResponse:
    def __init__(self, handled, mime_format="text/html", html_data=""):
        self.handled = handled
        self.mime_format = mime_format
        self.html_data = html_data


class URLParam:
    def __init__(self, name, caption, short_desc, html_desc="", disabled=False, html_tags=""):
        self.name = name
        self.caption = caption
        self.short_desc = short_desc
        self.html_desc = html_desc
        self.disabled = disabled
        self.html_tags = html_tags


class RestParam(URLParam):
    def __init__(self, path_name, caption, short_desc, html_desc="", html_tags=""):
        URLParam.__init__(self, path_name, caption, short_desc, html_desc, False, html_tags)

    def get_path_name(self):
        return self.name

    path_name = property(get_path_name)


def coordinates_to_html(list_of_coordinates, line_separator="<br>"):
    result = ""
    for line in list_of_coordinates:
        if result != "":
            result += line_separator
        result += line.y + ", " + line.x
    return result


def coordinates_to_json(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = "{"
    index = 0
    for line in list_of_coordinates:
        index += 1
        if index > 1:
            result += ','
        result += line_separator + '"' + tag + str(
            index) + '" : {' + line_separator + ' \t"Y": "' + line.y + '",' + line_separator + '\t"X": "' + line.x + '"' + line_separator + "\t}"
    result += line_separator + "}"
    return result


def coordinates_to_xml(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    index = 0
    for coordinates in list_of_coordinates:
        index = index + 1
        result += "<" + tag + str(
            index) + ">" + line_separator + "<Y>" + coordinates.y + "</Y>" + line_separator + "<X>" + coordinates.x + "</X>" + line_separator + "</" + tag + str(
            index) + ">" + line_separator
    result += "</xml>"
    return result


def coordinates_to_text(list_of_coordinates, line_separator="\n"):
    result = ""
    for line in list_of_coordinates:
        result += line.x + ", " + line.y + line_separator
    return result[:-1]


def addresses_to_xml(list_of_addresses, line_separator="\n", tag="Adresa"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator

    index = 0
    for line in list_of_addresses:
        orientation_number = none_to_string(line[6])
        sign = none_to_string(line[4])
        if orientation_number != "":
            house_numbers = "\t<" + sign + ">" + none_to_string(line[5]) + \
                            "</" + sign + ">" + line_separator + "\t<orientacni_cislo>" + \
                            orientation_number + none_to_string(line[7]) + "</orientacni_cislo>"
        else:
            house_numbers = "\t<" + sign + ">" + none_to_string(line[5]) + "</" + sign + ">"

        index = index + 1
        street = none_to_string(line[3])

        if street != "":
            street = "\t<ulice>" + street + "</ulice>" + line_separator

        town = none_to_string(line[1])
        district = none_to_string(line[2])

        if town == district or district == "":
            town_district = "\t<obec>" + town + "</obec>"
        else:
            town_district = "\t<obec>" + town + "</obec>" + line_separator + \
                            "\t<cast_obce>" + district + "</cast_obce>"

        result += "<" + tag + str(index) + ">" + line_separator + "<ID>" + none_to_string(line[0]) + \
                  "</ID>" + line_separator + town_district + line_separator + street + house_numbers + \
                  line_separator + "\t<PSČ>" + none_to_string(line[8]) + \
                  "</PSČ>" + line_separator + "</" + tag + str(index) + ">" + line_separator
    result += "</xml>"
    return result


def addresses_to_html(list_of_addresses, line_separator="\n", tag="Adresa"):
    result = addresses_to_xml(list_of_addresses, line_separator, tag)
    return result


def addresses_to_json(list_of_addresses, line_separator="\n", tag="Adresa"):
    out: str = "{"
    index = 0
    for line in list_of_addresses:
        index += 1
        if index > 1:
            out += ','

        orientation_number = none_to_string(line[6])
        sign = none_to_string(line[4])
        if orientation_number != "":
            house_numbers = '\t"' + sign + '": ' + none_to_string(
                line[5]) + ',' + line_separator + '\t"orientační_číslo":' + orientation_number + none_to_string(
                line[7]) + ','
        else:
            house_numbers = '\t"' + sign + '": ' + none_to_string(line[5]) + ','

        street = none_to_string(line[3])

        if street != "":
            street = '\t"ulice": ' + street + "," + line_separator

        town = none_to_string(line[1])
        district = none_to_string(line[2])

        if town == district or district == "":
            town_district = '\t"obec" : ' + town + ","
        else:
            town_district = '\t"obec" : ' + town + "," + line_separator + '\t"část_obce": ' + district + ","

        out += line_separator + '"' + tag + str(index) + '" : {' + line_separator + '\t"ID": ' + none_to_string(
            line[
                0]) + line_separator + town_district + line_separator + street + house_numbers + line_separator + '\t"PSČ" :' + none_to_string(
            line[8]) + line_separator + "\t}"
    out += line_separator + "}"
    return out


def addresses_to_text(list_of_addresses, line_separator="\n"):
    result = ""
    for line in list_of_addresses:
        orientation_number = none_to_string(line[6])
        if orientation_number != "":
            house_numbers = none_to_string(line[5]) + "/" + orientation_number + none_to_string(line[7])
        else:
            house_numbers = none_to_string(line[5])
        street = none_to_string(line[3])
        if street != "":
            street += " "
        town = none_to_string(line[1])
        district = none_to_string(line[2])
        if town == district:
            town_district = town
        else:
            town_district = town + "-" + district
        result += none_to_string(line[0]) + " " + street + none_to_string(
            line[4]) + " " + house_numbers + ", " + town_district + ", " + none_to_string(line[8]) + line_separator
    return result


def coordintes_to_response_text(format_text, list_of_coordinates):
    if format_text == TEXT_FORMAT_XML:
        return coordinates_to_xml(list_of_coordinates)
    elif format_text == TEXT_FORMAT_HTML:
        return coordinates_to_html(list_of_coordinates)
    elif format_text == TEXT_FORMAT_HTML2ONEROW:
        return coordinates_to_html(list_of_coordinates, "; ")
    elif format_text == TEXT_FORMAT_JSON:
        return coordinates_to_json(list_of_coordinates)
    elif format_text == TEXT_FORMAT_TEXT2ONEROW:
        return coordinates_to_text(list_of_coordinates, "; ")
    else:  # default value text
        return coordinates_to_text(list_of_coordinates)


def addresses_to_response_text(format_text, list_of_addresses):
    if format_text == TEXT_FORMAT_XML:
        return addresses_to_html(list_of_addresses)
    elif format_text == TEXT_FORMAT_HTML or format_text == TEXT_FORMAT_HTML2ONEROW:
        return addresses_to_text(list_of_addresses, LINE_SEPARATOR_HTML)
    elif format_text == TEXT_FORMAT_JSON:
        return addresses_to_json(list_of_addresses)
    else:  # default value text
        return addresses_to_text(list_of_addresses)


def get_mime_format(format_text):
    format_text = format_text.lower()
    if format_text in [TEXT_FORMAT_XML, TEXT_FORMAT_JSON]:
        return "application/" + format_text
    elif format_text in [TEXT_FORMAT_HTML, TEXT_FORMAT_HTML2ONEROW]:
        return "text/html"
    else:  # Default value text
        return "text/plain"


def p(query_params, name, def_value=""):
    if name in query_params:
        return parse.unquote(query_params[name])
    else:
        return def_value


def get_query_value(query_params, identifier, def_value):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu def_value
    return get_query_param(query_params, identifier, def_value)


def get_query_param(query_params, name, def_value=""):
    if name in query_params:
        return parse.unquote(query_params[name])
    else:
        return def_value


def extract_dictrict_number(nazev_mop):
    # Extracts district number for Prague: Praha 10 -> 10
    if (nazev_mop != "") and (nazev_mop is not None) and (nazev_mop.find(" ") >= 0):
        return nazev_mop.split(" ")[1]
    else:
        return ""


def item_to_str(item):
    # This function return str representation of item and if item is empty then empty string.
    if item is None:
        return ""
    else:
        return str(item)


if __name__ == "__main__":
    print("This is module file, it can not be run!")
