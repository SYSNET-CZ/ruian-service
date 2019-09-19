# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        validate
# Purpose:
#
# Author:      SYSNET
#
# Created:     13/11/2013
# Copyright:   (c) SYSNET 2019
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from service import ruian_connection

__author__ = 'SYSNET'


def build_validate_dict(street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
                        locality, locality_part, district_number):
    return {
        "street": street,
        "house_number": house_number,
        "record_number": record_number,
        "orientation_number": orientation_number,
        "orientation_number_character": orientation_number_character,
        "zip_code": str(zip_code).replace(" ", ""),
        "locality": locality,
        "locality_part": locality_part,
        "district_number": district_number
    }


def right_address(street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
                  locality, locality_part, district_number):
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
    if street == "" and house_number == "" and record_number == "" and orientation_number == "" and orientation_number_character == "" and psc == "" and locality == "" and locality_part == "" and district_number == "":
        return False
    return True


def validate_address(
        builder, street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number):
    if not right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number):
        return "False"

    dictionary = build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
        locality_part, district_number)

    result = ruian_connection.validateAddress(dictionary)
    return builder.listToResponseText(result)
