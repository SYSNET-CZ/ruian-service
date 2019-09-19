from service import ruian_connection, validate
from service.database import none_to_string


def compile_address(builder, street, house_number, record_number, orientation_number, orientation_number_character,
                    zip_code, locality, locality_part, district_number, do_validate=False, with_ruian_id=False):
    """
        @param street:                      string  Název ulice
        @param house_number:                number  Číslo popisné
        @param record_number:
        @param orientation_number:          number  Číslo orientační
        @param orientation_number_character string  Písmeno čísla orientačního
        @param zip_code:                    number  Poštovní směrovací číslo
        @param locality:                    string  Obec
        @param locality_part:               string  Část obce, pokud je známa
        @param district_number:
        @param do_validate:
        @param with_ruian_id:
        @param builder:
    """
    dictionary = validate.build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number)

    if do_validate or with_ruian_id:
        rows = ruian_connection.getAddresses(dictionary)

        if len(rows) == 1:
            (house_number, orientation_number, orientation_number_character, zip_code, locality, locality_part,
             nazev_mop, street, typ_so, ruian_id) = rows[0]
            if typ_so != "č.p.":
                record_number = house_number
                house_number = ""
            if nazev_mop is not None and nazev_mop != "":
                district_number = nazev_mop[nazev_mop.find(" ") + 1:]
            if not with_ruian_id:
                ruian_id = ""
        else:
            return ""
    else:
        ruian_id = ""

    if builder is None:
        return str((street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
                    locality, locality_part, district_number, ruian_id))
    elif builder.format_text == "json":
        return compile_address_as_json(street, house_number, record_number, orientation_number,
                                       orientation_number_character, zip_code, locality, locality_part,
                                       district_number, ruian_id)
    elif builder.formatText == "xml":
        return compile_address_as_xml(street, house_number, record_number, orientation_number,
                                      orientation_number_character, zip_code, locality, locality_part,
                                      district_number, ruian_id)
    elif builder.formatText == "texttoonerow" or builder.formatText == "htmltoonerow":
        return compile_address_to_one_row(street, house_number, record_number, orientation_number,
                                          orientation_number_character, zip_code, locality, locality_part,
                                          district_number, ruian_id)
    else:
        return builder.list_to_response_text(
            compile_address_as_text(street, house_number, record_number, orientation_number,
                                    orientation_number_character, zip_code, locality, locality_part,
                                    district_number, ruian_id))


def list_to_xml(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    for line in list_of_lines:
        result += "<" + tag + ">" + line_separator + line + "</" + tag + ">" + line_separator
    return result + "</xml>"


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


def dictionary_to_text(dictionary, with_id, with_address):
    response = dictionary["JTSKY"] + ", " + dictionary["JTSKX"]
    if with_id:
        response = dictionary["id"] + ", " + response
    if with_address:
        response += ", " + compile_address_to_one_row(dictionary["street"], dictionary["house_number"],
                                                      dictionary["record_number"], dictionary["orientation_number"],
                                                      dictionary["orientation_number_character"],
                                                      dictionary["zip_code"],
                                                      dictionary["locality"], dictionary["locality_part"],
                                                      dictionary["district_number"])
    return response


def dictionary_to_xml(dictionary, with_id, with_address):
    response = "<record>\n"
    if with_id:
        response += "\t<id>" + dictionary["id"] + "</id>\n"
    response += "\t<JTSKY>" + dictionary["JTSKY"] + "</JTSKY>\n"
    response += "\t<JTSKX>" + dictionary["JTSKX"] + "</JTSKX>\n"
    if with_address:
        response += compile_address_as_xml(dictionary["street"], dictionary["house_number"],
                                           dictionary["record_number"],
                                           dictionary["orientation_number"], dictionary["orientation_number_character"],
                                           dictionary["zip_code"], dictionary["locality"], dictionary["locality_part"],
                                           dictionary["district_number"])
    response += "</record>\n"
    return response


def dictionary_to_json(dictionary, with_id, with_address):
    response = "\n\t{\n"
    if with_id:
        response += '\t"id":' + dictionary["id"] + ",\n"
    response += '\t"JTSKY":' + dictionary["JTSKY"] + ",\n"
    response += '\t"JTSKX":' + dictionary["JTSKX"]
    if with_address:
        response += ",\n" + compile_address_as_json(dictionary["street"], dictionary["house_number"],
                                                    dictionary["record_number"],
                                                    dictionary["orientation_number"],
                                                    dictionary["orientation_number_character"],
                                                    dictionary["zip_code"], dictionary["locality"],
                                                    dictionary["locality_part"],
                                                    dictionary["district_number"])
    else:
        response += "\n"
    response += "\t}"
    return response


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


def coordinates_to_html(list_of_coordinates, line_separator="<br>"):
    result = ""
    for line in list_of_coordinates:
        if result != "":
            result += line_separator
        result += line.JTSKY + ", " + line.JTSKX
    return result


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


def addresses_to_json(list_of_addresses, line_separator="\n", tag="Adresa"):
    result = "{"
    index = 0
    for line in list_of_addresses:
        index += 1
        if index > 1:
            result += ','

        orientation_number = none_to_string(line[6])
        sign = none_to_string(line[4])
        if orientation_number != "":
            house_numbers = '\t"' + sign + '": ' + none_to_string(line[5]) + ',' + line_separator + \
                            '\t"orientační_číslo":' + orientation_number + \
                            none_to_string(line[7]) + ','
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

        result += line_separator + '"' + tag + str(index) + '" : {' + line_separator + '\t"ID": ' + none_to_string(
            line[
                0]) + line_separator + town_district + line_separator + street + house_numbers + line_separator + '\t"PSČ" :' + none_to_string(
            line[8]) + line_separator + "\t}"
    result += line_separator + "}"
    return result


def addresses_to_text(list_of_addresses, line_separator="\n"):
    result = ""
    for line in list_of_addresses:
        orientation_number = str(none_to_string(line[6]))
        if orientation_number != "":
            house_numbers = str(none_to_string(line[5])) + "/" + orientation_number + str(none_to_string(line[7]))
        else:
            house_numbers = str(none_to_string(line[5]))
        street = none_to_string(line[3])
        if street != "":
            street += " "
        town = none_to_string(line[1])
        district = none_to_string(line[2])
        if town == district:
            town_district = town
        else:
            town_district = town + "-" + district
        result = str(result)
        result += str(none_to_string(line[0]))
        result += " " + street
        result += str(none_to_string(line[4]))
        result += " " + str(house_numbers)
        result += ", " + town_district
        result += ", " + str(none_to_string(line[8]))
        result += line_separator
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


class MimeBuilder:
    def __init__(self, format_text="text"):
        self.format_text = format_text.lower()
        self.record_separator = "\n"

        if self.format_text in ["xml", "json"]:
            self.line_separator = "\n"
        elif self.format_text == "html":
            self.line_separator = "<br>"
        elif self.format_text in ["htmltoonerow", "texttoonerow"]:
            self.line_separator = ", "
        else:  # default value text
            self.line_separator = "\n"

        pass

    def get_mime_format(self):
        if self.format_text in ["xml", "json"]:
            return "application/" + self.format_text
        elif self.format_text in ["html", "htmltoonerow"]:
            return "text/html"
        else:  # Default value text
            return "text/plain"

    def list_to_response_text(self, list_of_lines, ignore_one_row=False, record_separator="\n"):
        if record_separator == "":
            line_separator = self.line_separator
        else:
            line_separator = record_separator
        work_list = list_of_lines
        if ignore_one_row:
            work_list = list_of_lines[1:]

        if self.format_text == "xml":
            return list_to_xml(work_list, line_separator)
        elif self.format_text == "html" or self.format_text == "htmltoonerow":
            return list_to_html(work_list, line_separator)
        elif self.format_text == "json":
            return list_to_json(work_list, line_separator)
        else:  # default value text
            return list_to_text(work_list, line_separator)

    def list_of_dictionaries_to_response_text(self, list_of_dictionaries, with_id, with_address):
        response = ""
        if self.format_text == "xml":
            head = '<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n'
            body = ""
            tail = "</xml>"
            for dictionary in list_of_dictionaries:
                body += dictionary_to_xml(dictionary, with_id, with_address)
            return head + body + tail
        elif self.format_text == "json":
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
                response += dictionary_to_text(dictionary, with_id, with_address) + self.line_separator
            response = response[:-len(self.line_separator)]
        return response

    def coordintes_to_response_text(self, list_of_coordinates):
        if self.format_text == "xml":
            return coordinates_to_xml(list_of_coordinates)
        elif self.format_text == "html":
            return coordinates_to_html(list_of_coordinates)
        elif self.format_text == "htmltoonerow":
            return coordinates_to_html(list_of_coordinates, "; ")
        elif self.format_text == "json":
            return coordinates_to_json(list_of_coordinates)
        elif self.format_text == "texttoonerow":
            return coordinates_to_text(list_of_coordinates, "; ")
        else:  # default value text
            return coordinates_to_text(list_of_coordinates)

    def addresses_to_response_text(self, list_of_addresses):
        if self.format_text == "xml":
            return addresses_to_xml(list_of_addresses)
        elif self.format_text == "html" or self.format_text == "htmltoonerow":
            return addresses_to_text(list_of_addresses, "<br>")
        elif self.format_text == "json":
            return addresses_to_json(list_of_addresses)
        else:  # default value text
            return addresses_to_text(list_of_addresses)


class TextFormat:
    plain_text = 0
    xml = 1
    json = 2
    html = 3


def compile_address_as_text(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
        locality_part, district_number, ruian_id=""):
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
        # Convert None values to "".
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, ruian_id) = none_to_string(
            (street, house_number, record_number, orientation_number,
             orientation_number_character, zip_code, locality, locality_part, district_number, ruian_id))

        zip_code = format_zip_code(zip_code)
        house_number = number_check(house_number)
        orientation_number = number_check(orientation_number)
        district_number = number_check(district_number)
        orientation_number_character = alpha_check(orientation_number_character)

        town_info = zip_code + " " + locality

        if district_number != "":
            town_info += " " + district_number

        if house_number != "":
            house_numberStr = " " + house_number
            if orientation_number != "":
                house_numberStr += u"/" + orientation_number + orientation_number_character
        elif record_number != "":
            house_numberStr = u" č.ev. " + record_number
        else:
            house_numberStr = ""

        if locality.upper() == "PRAHA":
            if street != "":
                lines.append(street + house_numberStr)
                lines.append(locality_part)
                lines.append(town_info)
            else:
                lines.append(locality_part + house_numberStr)
                lines.append(town_info)
        else:
            if street != "":
                lines.append(street + house_numberStr)
                if locality_part != locality:
                    lines.append(locality_part)
                lines.append(town_info)
            else:
                if locality_part != locality:
                    lines.append(locality_part + house_numberStr)
                else:
                    if house_number != "":
                        lines.append(u"č.p." + house_numberStr)
                    else:
                        lines.append(house_numberStr[1:])
                lines.append(town_info)

        if ruian_id != "":
            lines.insert(0, str(ruian_id))
    except (ValueError, Exception) as e:
        print(str(e))
        pass
    return lines


def compile_address_as_json(street, house_number, record_number, orientation_number, orientation_number_character,
                            zip_code, locality, locality_part, district_number, ruian_id=""):
    (street, house_number, record_number, orientation_number, orientation_number_character,
     zip_code, locality, locality_part, district_number, ruian_id) = \
        none_to_string((street, house_number, record_number, orientation_number, orientation_number_character,
                        zip_code, locality, locality_part, district_number, ruian_id))
    if house_number != "":
        sign = u"č.p."
        address_number = house_number
    else:
        sign = u"č.ev."
        address_number = record_number

    if orientation_number != "":
        house_number_str = '\t"' + sign + '": ' + address_number + ',\n\t"orientační_číslo": ' + \
                           orientation_number + orientation_number_character + ','
    else:
        house_number_str = '\t"' + sign + '":"%s", ' % address_number

    if street != "":
        street = '\t"ulice": "%s",\n' % street

    if district_number != "":
        district_number_str = ',\n\t"číslo_městského_obvodu": %s,\n ' % district_number
    else:
        district_number_str = ""

    if locality == locality_part or locality_part == "":
        town_district = '\t"obec":"%s"%s' % (locality, district_number_str)
    else:
        town_district = '\t"obec": "%s"%s\t"část_obce": "%s" ' % (locality, district_number_str, locality_part)

    if ruian_id != "":
        ruian_id_text = '\t"ruian_id": %s,\n' % ruian_id
    else:
        ruian_id_text = ""

    result = ruian_id_text + street + house_number_str + '\n\t"PSČ": "%s",\n%s\n' % (zip_code, town_district)
    return result


def compile_address_as_xml(street, house_number, record_number, orientation_number, orientation_number_character,
                           zip_code, locality, locality_part, district_number, ruian_id=""):
    (street, house_number, record_number, orientation_number, orientation_number_character,
     zip_code, locality, locality_part, district_number, ruian_id) = \
        none_to_string((street, house_number, record_number, orientation_number, orientation_number_character,
                        zip_code, locality, locality_part, district_number, ruian_id))
    if house_number != "":
        sign = "c.p."
        address_number = house_number
    else:
        sign = "c.ev."
        address_number = record_number

    if orientation_number != "":
        house_number_str = '\t<' + sign + '>' + address_number + '</' + sign + '>\n\t<orientacni_cislo>' + \
                           orientation_number + orientation_number_character + '</orientacni_cislo>'
    else:
        house_number_str = '\t<' + sign + '>' + address_number + '</' + sign + '>'

    if street != "":
        street = '\t<ulice>' + street + "</ulice>\n"

    if district_number != "":
        district_number_str = '\n\t<cislo_mestskeho_obvodu>' + district_number + '</cislo_mestskeho_obvodu>'
    else:
        district_number_str = ""

    if locality == locality_part or locality_part == "":
        town_district = '\t<obec>' + locality + "</obec>" + district_number_str
    else:
        town_district = '\t<obec>' + locality + '</obec>' + district_number_str + \
                        '\n\t<cast_obce>' + locality_part + '</cast_obce>'

    if ruian_id != "":
        ruian_id_str = "\t<ruian_id>%s</ruian_id>\n" % ruian_id
    else:
        ruian_id_str = ""

    result = street + house_number_str + '\n\t<PSC>' + zip_code + "</PSC>\n" + town_district + "\n" + ruian_id_str
    return result


def compile_address_to_one_row(street, house_number, record_number, orientation_number, orientation_number_character,
                               zip_code, locality, locality_part, district_number, ruian_id=""):
    street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality, locality_part, district_number, ruian_id = none_to_string(
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, ruian_id))

    addressStr = ""
    zip_code = format_zip_code(zip_code)
    house_number = empty_string_if_no_number(house_number)
    orientation_number = empty_string_if_no_number(orientation_number)
    district_number = empty_string_if_no_number(district_number)
    orientation_number_character = alpha_check(orientation_number_character)

    townInfo = zip_code + " " + locality  # unicode(locality, "utf-8")
    if district_number != "":
        townInfo += " " + district_number

    if house_number != "":
        house_numberStr = " " + house_number
        if orientation_number != "":
            house_numberStr += u"/" + orientation_number + orientation_number_character
    elif record_number != "":
        house_numberStr = u" č.ev. " + record_number
    else:
        house_numberStr = ""

    if locality.upper() == "PRAHA":
        if str_is_not_empty(street):
            addressStr += street + house_numberStr + ", " + locality_part + ", " + townInfo
        else:
            addressStr += locality_part + house_numberStr + ", " + townInfo
    else:
        if str_is_not_empty(street):
            addressStr += street + house_numberStr + ", "
            if locality_part != locality:
                addressStr += locality_part + ", "
            addressStr += townInfo
        else:
            if locality_part != locality:
                addressStr += locality_part + house_numberStr + ", "
            else:
                if house_number != "":
                    addressStr += u"č.p." + house_numberStr + ", "
                else:
                    addressStr += house_numberStr[1:] + ", "
            addressStr += townInfo

    if ruian_id != "":
        addressStr = "%s, %s" % (str(ruian_id), addressStr)

    return addressStr


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


def empty_string_if_no_number(possible_number):
    if possible_number is not None:
        if str(possible_number).isdigit():
            return str(possible_number)
        else:
            return ""
    else:
        return ""


def alpha_check(possible_alpha):
    if possible_alpha is not None:
        if possible_alpha.isalpha():
            return possible_alpha
        else:
            return ""
    else:
        return ""


def str_is_not_empty(v):
    return v is not None and v != ""


def number_check(possible_number):
    if possible_number is not None and str(possible_number).isdigit():
        return str(possible_number)
    else:
        return ""
