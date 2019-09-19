# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         models
# Purpose:      Models udes in the service
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------

__author__ = 'SYSNET'


class Coordinates:
    # JTSK
    def __init__(self, y, x):
        self.x = x
        self.y = y


class Address:
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number):
        self.street = street
        self.houseNumber = house_number
        self.recordNumber = record_number
        self.orientationNumber = orientation_number
        self.orientationNumberCharacter = orientation_number_character
        self.zipCode = zip_code
        self.locality = locality
        self.localityPart = locality_part
        self.districtNumber = district_number


class Locality:
    coordinates: object

    def __init__(self, address, coordinates):
        self.address = address
        self.coordinates = coordinates
