# -*- coding: utf-8 -*-


def list_to_xml(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    for line in list_of_lines:
        result += "<" + tag + ">" + line_separator + line + "</" + tag + ">" + line_separator
    return result + "</xml>"


def list_to_text(list_of_lines, line_separator="\n"):
    result = ""
    for line in list_of_lines:
        result += line + line_separator
    return result[:-len(line_separator)]


def list_to_html(list_of_lines, line_separator="<br>"):
    result = ""
    for line in list_of_lines:
        if result != "":
            result += line_separator
        result += line
    return result


def coordinates_to_html(list_of_coordinates, line_separator="<br>"):
    result = ""
    for line in list_of_coordinates:
        if result != "":
            result += line_separator
        result += line.JTSKY + ", " + line.JTSKX
    return result


def addresses_to_xxx(list_of_addresses, line_separator="\n"):
    result = ""
    for line in list_of_addresses:
        print(str(line) + line_separator)
    return result


def coordinates_to_text(list_of_coordinates, line_separator="\n"):
    result = ""
    for line in list_of_coordinates:
        result += line.x + ", " + line.y + line_separator
    return result[:-1]


def coordinates_to_json(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = "{"
    index = 0
    for line in list_of_coordinates:
        index += 1
        if index > 1:
            result += ','
        result += line_separator + '"' + tag + str(index) + (
                '" : {' + line_separator + ' \t"Y": "' + line.y + '",') + (
                          line_separator + '\t"X": "' + line.x + '"' + line_separator + "\t}")
    result += line_separator + "}"
    return result


class TextFormat:
    plain_text = 0
    xml = 1
    json = 2
    html = 3


def format_zip_code(code):
    if code is None:
        return ""
    else:
        code = str(code)
        code = code.replace(" ", "")
        if code.isdigit():
            return code
        else:
            return ""


def number_check(possible_number):
    if possible_number is not None and str(possible_number).isdigit():
        return str(possible_number)
    else:
        return ""


def is_int(value):
    if value is None:
        return False
    if value == "":
        return False
    else:
        for i in range(len(value)):
            if "0123456789".find(value[i:i + 1]) < 0:
                return False
        return True
