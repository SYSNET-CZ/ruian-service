# -*- coding: utf-8 -*-
import json

import dicttoxml

from service.models import none_to_string, formatzip_code, empty_string_if_no_number, alpha_check, PrettyAddress

TEXT_FORMAT_JSON = "json"
TEXT_FORMAT_XML = "xml"
TEXT_FORMAT_HTML = "html"
TEXT_FORMAT_TEXT = "text"
TEXT_FORMAT_TEXT2ONEROW = "texttoonerow"
TEXT_FORMAT_HTML2ONEROW = "htmltoonerow"
RECORD_SEPARATOR = "\n"
LINE_SEPARATOR = "\n"
LINE_SEPARATOR_TEXT = "\n"
LINE_SEPARATOR_XML = "\n"
LINE_SEPARATOR_JSON = "\n"
LINE_SEPARATOR_HTML = "<br />"
LINE_SEPARATOR_ROW = ", "


def compile_address_as_dictionary_cz(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    work = compile_address_as_dictionary_en(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id)
    out = {}
    if "house_number" in work:
        out["č.p."] = work["house_number"]
    if "record_number" in work:
        out["č.ev."] = work["record_number"]
    if "orientation_number" in work:
        out["orientační_číslo"] = work["orientation_number"]
    if "street" in work:
        out["ulice"] = work["street"]
    if "district_number" in work:
        out["číslo_městského_obvodu"] = work["district_number"]
    if "locality" in work:
        out["obec"] = work["locality"]
    if "locality_part" in work:
        out["část_obce"] = work["locality_part"]
    if "ruian_id" in work:
        out["ruian_id"] = work["ruian_id"]
    return out


def compile_address_as_dictionary_en(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    (
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id) = none_to_string(
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
         locality, locality_part, district_number, ruian_id))
    out = {}
    if house_number != "":
        sign = "house_number"
        address_number = house_number
    else:
        sign = "record_number"
        address_number = record_number
    if orientation_number != "":
        out[sign] = address_number
        out["orientation_number"] = orientation_number + orientation_number_character
    else:
        out[sign] = address_number
    if street != "":
        out["street"] = street
    if district_number != "":
        out["district_number"] = district_number
    else:
        out["district_number"] = ""

    if locality == locality_part or locality_part == "":
        out["locality"] = "%s %s" % (locality, str(district_number))
    else:
        out["locality"] = "%s %s" % (locality, str(district_number))
        out["locality_part"] = locality_part
    if ruian_id != "":
        out["ruian_id"] = ruian_id
    return out


def compile_address_as_json(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    out = compile_address_as_dictionary_cz(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id)
    return json.dumps(out)


def compile_address_as_xml(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    out = compile_address_as_dictionary_en(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id)
    xml = dicttoxml.dicttoxml(out, attr_type=False, custom_root='adresa')
    return xml


def compile_address_as_text_experimental(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    out = compile_address_as_dictionary_en(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id)
    out_str = ""
    if "street" in out:
        out_str += out["street"]

    return out_str


def compile_address_to_one_row(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality, locality_part, district_number, ruian_id = none_to_string(
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
         locality, locality_part, district_number, ruian_id))

    address_str = ""
    zip_code = formatzip_code(zip_code)
    house_number = empty_string_if_no_number(house_number)
    orientation_number = empty_string_if_no_number(orientation_number)
    district_number = empty_string_if_no_number(district_number)
    orientation_number_character = alpha_check(orientation_number_character)

    town_info = zip_code + " " + locality
    # unicode(locality, "utf-8")
    if district_number != "":
        town_info += " " + district_number

    if house_number != "":
        house_number_str = " " + house_number
        if orientation_number != "":
            house_number_str += u"/" + orientation_number + orientation_number_character
    elif record_number != "":
        house_number_str = u" č.ev. " + record_number
    else:
        house_number_str = ""

    if locality.upper() == "PRAHA":
        if str_is_not_empty(street):
            address_str += street + house_number_str + ", " + locality_part + ", " + town_info
        else:
            address_str += locality_part + house_number_str + ", " + town_info
    else:
        if str_is_not_empty(street):
            address_str += street + house_number_str + ", "
            if locality_part != locality:
                address_str += locality_part + ", "
            address_str += town_info
        else:
            if locality_part != locality:
                address_str += locality_part + house_number_str + ", "
            else:
                if house_number != "":
                    address_str += u"č.p." + house_number_str + ", "
                else:
                    address_str += house_number_str[1:] + ", "
            address_str += town_info

    if ruian_id != "":
        address_str = "%s, %s" % (str(ruian_id), address_str)

    return address_str


def str_is_not_empty(v):
    return v is not None and v != ""


def compile_address_as_text(street, house_number, record_number, orientation_number, orientation_number_character,
                            zip_code, locality, locality_part, district_number, district_name, ruian_id=""):
    """
    Sestaví adresu dle hodnot v parametrech, prázdný parametr je "" nebo None.

    @param: street : String                     Jméno ulice
    @param: house_number : String                Číslo popisné
    @param: record_number : String               Číslo evidenční
    @param: orientation_number : String          Číslo orientační
    @param: orientation_number_character : String Písmeno čísla orientačního
    @param: zip_code : object String             Poštovní směrovací číslo
    @param: locality : object String            Obec
    @param: locality_part : String Street        Část obce
    @param: district_number : String             Číslo městského obvodu v Praze
    """
    lines = []  # Result list, initiated for case of error

    try:
        pretty_address = PrettyAddress(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number, district_name, ruian_id)
        lines = pretty_address.get_lines()
    except (ValueError, Exception) as e:
        print(e.pgerror)
        pass
    return lines


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


def number_to_string(number):
    # This function return str representation of item and if item is empty then empty string.
    if number is None:
        return ""
    else:
        return str(number)


def right_address(street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
                  locality, locality_part, district_number, district_name):
    psc = zip_code.replace(" ", "")
    if house_number != "" and not house_number.isdigit():
        return False
    if orientation_number != "" and not orientation_number.isdigit():
        return False
    if record_number != "" and not record_number.isdigit():
        return False
    if orientation_number_character != "" and not orientation_number_character.isalpha():
        return False
    if psc != "" and not psc.isdigit():
        return False
    if district_number != "" and not district_number.isdigit():
        return False
    if street == "" and \
            house_number == "" and \
            record_number == "" and \
            orientation_number == "" and \
            orientation_number_character == "" and \
            psc == "" and \
            locality == "" and \
            locality_part == "" and \
            district_number == "" and \
            district_name == "":
        return False
    return True


def list_to_response_text(text_format, list_of_lines):
    # TODO prověřit, zda bude potřeba
    if text_format == TEXT_FORMAT_XML:
        return list_to_xml(list_of_lines, LINE_SEPARATOR_XML)
    elif text_format == TEXT_FORMAT_HTML:
        return list_to_html(list_of_lines, LINE_SEPARATOR_HTML)
    elif text_format == TEXT_FORMAT_HTML2ONEROW:
        return list_to_html(list_of_lines, LINE_SEPARATOR_ROW)
    elif text_format == TEXT_FORMAT_JSON:
        return list_to_json(list_of_lines, LINE_SEPARATOR_JSON)
    elif text_format == TEXT_FORMAT_TEXT2ONEROW:
        return list_to_text(list_of_lines, LINE_SEPARATOR_ROW)
    else:  # default value text
        return list_to_text(list_of_lines, LINE_SEPARATOR_TEXT)


def list_to_xml(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    # TODO prověřit, zda bude potřeba
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    for line in list_of_lines:
        result += "<" + tag + ">" + line_separator + line + "</" + tag + ">" + line_separator
    return result + "</xml>"


def list_to_html(list_of_lines, line_separator="<br>"):
    # TODO prověřit, zda bude potřeba
    result = ""
    for line in list_of_lines:
        if result != "":
            result += line_separator
        result += line
    return result


def list_to_text(list_of_lines, line_separator="\n"):
    result = ""
    for line in list_of_lines:
        result += line + line_separator
    return result[:-len(line_separator)]


def list_to_json(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = "{"
    index = 0
    for item in list_of_lines:
        index += 1
        if index > 1:
            result += ','
        if item == "True" or item == "False":
            addition1 = '\t"valid" : '
            addition2 = "\n"
        else:
            addition1 = ""
            addition2 = ""
        result += line_separator + '"' + tag + str(
            index) + '" : {' + line_separator + addition1 + item + addition2 + "\t}"
    result += line_separator + "}"
    return result


def list_of_dictionaries_to_response_text(format_text, list_of_dictionaries, with_id, with_address):
    response = ""
    if format_text == TEXT_FORMAT_XML:
        head = '<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n'
        body = ""
        tail = "</xml>"
        for dictionary in list_of_dictionaries:
            body += dictionary_to_xml(dictionary, with_id, with_address)
        return head + body + tail
    elif format_text == TEXT_FORMAT_JSON:
        head = '{\n"records": ['
        body = ""
        tail = "\n]}"
        first = True
        for dictionary in list_of_dictionaries:
            if first:
                first = False
            else:
                body += ","
            body += dictionary_to_json(dictionary, with_id, with_address)
        return head + body + tail
    else:
        for dictionary in list_of_dictionaries:
            response += dictionary_to_text(dictionary, with_id, with_address) + LINE_SEPARATOR_TEXT
        response = response[:-len(LINE_SEPARATOR_TEXT)]
    return response


def dictionary_to_json(dictionary, with_id, with_address):
    response = "\n\t{\n"
    if with_id:
        response += '\t"id":' + dictionary["id"] + ",\n"
    response += '\t"y":' + dictionary["y"] + ",\n"
    response += '\t"x":' + dictionary["x"]
    if with_address:
        response += ",\n" + compile_address_as_json(
            dictionary["street"], dictionary["house_number"], dictionary["record_number"],
            dictionary["orientation_number"],
            dictionary["orientation_number_character"], dictionary["zip_code"], dictionary["locality"],
            dictionary["locality_part"], dictionary["district_number"])
    else:
        response += "\n"
    response += "\t}"
    return response


def dictionary_to_xml(dictionary, with_id, with_address):
    response = "<record>\n"
    if with_id:
        response += "\t<id>" + dictionary["id"] + "</id>\n"
    response += "\t<y>" + dictionary["y"] + "</y>\n"
    response += "\t<x>" + dictionary["x"] + "</x>\n"
    if with_address:
        response += compile_address_as_xml(
            dictionary["street"], dictionary["house_number"], dictionary["record_number"],
            dictionary["orientation_number"],
            dictionary["orientation_number_character"], dictionary["zip_code"], dictionary["locality"],
            dictionary["locality_part"], dictionary["district_number"])
    response += "</record>\n"
    return response


def dictionary_to_text(dictionary, with_id, with_address):
    response = dictionary["y"] + ", " + dictionary["x"]
    if with_id:
        response = dictionary["id"] + ", " + response
    if with_address:
        response += ", " + compile_address_to_one_row(
            dictionary["street"], dictionary["house_number"], dictionary["record_number"],
            dictionary["orientation_number"], dictionary["orientation_number_character"],
            dictionary["zip_code"], dictionary["locality"],
            dictionary["locality_part"], dictionary["district_number"])
    return response
