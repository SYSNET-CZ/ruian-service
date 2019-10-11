# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         models
# Purpose:      Models udes in the service
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
import json

__author__ = 'SYSNET'


class Coordinates:
    # JTSK
    def __init__(self, y, x):
        self.x = x
        self.y = y


class CoordinatesGps:
    # WGS
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


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


class Parcela:
    id: int  # 00 parcely.id,
    kmenovecislo: int  # 01 parcely.kmenovecislo,
    pododdelenicisla: int  # 02 parcely.pododdelenicisla,
    vymeraparcely: int  # 03 parcely.vymeraparcely,
    ku_kod: int  # 04 parcely.katastralniuzemikod,
    ku_nazev: str  # 05 katastralniuzemi.nazev,
    obec_kod: int  # 06 katastralniuzemi.obeckod,
    obec_nazev: str  # 07 obce.nazev,
    obec_statuskod: int  # 08 obce.statuskod,
    okres_kod: int  # 09 obce.okreskod,
    pou_kod: int  # 10 obce.poukod,
    okres_nazev: str  # 11 okresy.nazev,
    kraj_kod: int  # 12 okresy.krajkod,
    vusc_kod: int  # 13 okresy.vusckod,
    pou_nazev: str  # 14 pou.nazev,
    orp_kod: int  # 15 pou.orpkod, (Decimal)
    kraj_nazev: str  # 16 kraje.nazev,
    stat_kod: int  # 17 kraje.statkod,
    vusc_nazev: str  # 18 vusc.nazev,
    regionsoudrznosti_kod: int  # 19 vusc.regionsoudrznostikod,
    vusc_nutslau: str  # 20 vusc.nutslau,
    orp_nazev: str  # 21 orp.nazev,
    stat_nazev: str  # 22 staty.nazev,
    stat_nutslau: str  # 23 staty.nutslau,
    regionsoudrznosti_nazev: str  # 24 regionysoudrznosti.nazev,
    regionsoudrznosti_nutslau: str  # 25 regionysoudrznosti.nutslau

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.kmenovecislo = row[1]
            self.pododdelenicisla = row[2]
            self.vymeraparcely = row[3]
            self.ku_kod = row[4]
            self.ku_nazev = row[5]
            self.obec_kod = row[6]
            self.obec_nazev = row[7]
            self.obec_statuskod = row[8]
            self.okres_kod = row[9]
            self.pou_kod = row[10]
            self.okres_nazev = row[11]
            self.kraj_kod = row[12]
            self.vusc_kod = row[13]
            self.pou_nazev = row[14]
            self.orp_kod = int(row[15])
            self.kraj_nazev = row[16]
            self.stat_kod = row[17]
            self.vusc_nazev = row[18]
            self.regionsoudrznosti_kod = row[19]
            self.vusc_nutslau = row[20]
            self.orp_nazev = row[21]
            self.stat_nazev = row[22]
            self.stat_nutslau = row[23]
            self.regionsoudrznosti_nazev = row[24]
            self.regionsoudrznosti_nutslau = row[25]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Povodi:
    id: int  # 00
    chp: str  # 01
    chp_u: str  # 02
    chp_d: str  # 03
    naz_tok: str  # 04
    naz_tok_2: str  # 05
    id_3: int  # 06
    naz_pov_3: str  # 07
    id_2: int  # 08
    naz_pov_2: str  # 09
    id_1: int  # 10
    naz_pov_1: str  # 11
    # wgs: CoordinatesGps
    # jtsk: Coordinates

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.chp = row[1]
            self.chp_u = row[2]
            self.chp_d = row[3]
            self.naz_tok = row[4]
            self.naz_tok_2 = row[5]
            self.id_3 = row[6]
            self.naz_pov_3 = row[7]
            self.id_2 = row[8]
            self.naz_pov_2 = row[9]
            self.id_1 = row[10]
            self.naz_pov_1 = row[11]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
