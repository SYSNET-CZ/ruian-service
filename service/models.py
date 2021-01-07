# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         models
# Purpose:      Models used in the service
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
import json

__author__ = 'SYSNET'


class Coordinates(dict, object):
    # JTSK (5514)
    x: float
    y: float

    def __init__(self, y, x):
        dict.__init__(self, y=y, x=x)
        self.x = abs(x) * -1
        self.y = abs(y) * -1
        dict.__init__(self, y=self.y, x=self.x)

        # This field will not be sent in the response
        # self.status = 'active'


class CoordinatesGps(dict, object):
    # WGS
    lat: float
    lon: float

    def __init__(self, lat, lon):
        dict.__init__(self, lat=lat, lon=lon)
        self.lat = lat
        self.lon = lon


class Address(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id):
        dict.__init__(
            self, street=street, house_number=house_number, record_number=record_number,
            orientation_number=orientation_number, orientation_number_character=orientation_number_character,
            zip_code=zip_code, locality=locality, locality_part=locality_part, district_number=district_number,
            district=district, ruian_id=ruian_id
        )
        self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.orientation_number_character = orientation_number_character
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.district = district
        self.ruian_id = ruian_id

    def to_pretty(self):
        out = PrettyAddress(
            self.street, self.house_number, self.record_number, self.orientation_number,
            self.orientation_number_character, self.zip_code, self.locality, self.locality_part,
            self.district_number, self.district, self.ruian_id
        )
        return out


class PrettyAddress(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id):
        # Convert None values to "".
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, district, ruian_id) = none_to_string(
            (street, house_number, record_number, orientation_number,
             orientation_number_character, zip_code, locality, locality_part, district_number, district, ruian_id))

        self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.orientation_number_character = orientation_number_character
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.district = district
        self.ruian_id = ruian_id

        self.zip_code = formatzip_code(self.zip_code)
        self.house_number = empty_string_if_no_number(self.house_number)
        self.orientation_number = empty_string_if_no_number(self.orientation_number)
        self.district_number = empty_string_if_no_number(self.district_number)
        self.orientation_number_character = alpha_check(self.orientation_number_character)
        self.town_info = self.zip_code + " " + self.locality
        if self.district_number != "":
            self.town_info += " " + self.district_number
        if self.house_number != "":
            self.house_number_str = " " + self.house_number
            if self.orientation_number != "":
                self.house_number_str += u"/" + self.orientation_number + self.orientation_number_character
        elif self.record_number != "":
            self.house_number_str = u" č.ev. " + self.record_number
        else:
            self.house_number_str = ""
        dict.__init__(
            self, street=self.street, house_number=self.house_number, record_number=self.record_number,
            orientation_number=self.orientation_number, orientation_number_character=self.orientation_number_character,
            zip_code=self.zip_code, locality=self.locality, locality_part=self.locality_part,
            district_number=self.district_number, district=self.district,
            ruian_id=self.ruian_id, town_info=self.town_info,
            house_number_str=self.house_number_str
        )

    def get_lines(self):
        lines = []  # Result list, initiated for case of error
        if self.locality.upper() == "PRAHA":
            if self.street != "":
                lines.append(self.street + self.house_number_str)
                lines.append(self.locality_part)
                lines.append(self.town_info)
            else:
                lines.append(self.locality_part + self.house_number_str)
                lines.append(self.town_info)
        else:
            if self.street != "":
                lines.append(self.street + self.house_number_str)
                if self.locality_part != self.locality:
                    lines.append(self.locality_part)
                lines.append(self.town_info)
            else:
                if self.locality_part != self.locality:
                    lines.append(self.locality_part + self.house_number_str)
                else:
                    if self.house_number != "":
                        lines.append(u"č.p." + self.house_number_str)
                    else:
                        lines.append(self.house_number_str[1:])
                lines.append(self.town_info)
        if self.ruian_id != "":
            lines.insert(0, str(self.ruian_id))

        return lines

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


class Locality(dict, object):
    coordinates: Coordinates
    address: Address

    def __init__(self, address, coordinates):
        dict.__init__(self, address=address, coordinates=coordinates)
        self.address = address
        self.coordinates = coordinates


class MapovyList50:
    id: str
    nazev: str

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.nazev = row[2]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


class KatastralniUzemi:
    id: int
    nazev: str
    obec_kod: int
    obec_nazev: str
    obec_statuskod: int
    okres_kod: int
    pou_kod: int
    okres_nazev: str
    kraj_kod: int
    vusc_kod: int
    pou_nazev: str
    orp_kod: int
    kraj_nazev: str
    stat_kod: int
    vusc_nazev: str
    regionsoudrznosti_kod: int
    vusc_nutslau: str
    orp_nazev: str
    stat_nazev: str
    stat_nutslau: str
    regionsoudrznosti_nazev: str
    regionsoudrznosti_nutslau: str

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.nazev = row[1]
            self.obec_kod = row[2]
            self.obec_nazev = row[3]
            self.obec_statuskod = row[4]
            self.okres_kod = row[5]
            self.pou_kod = row[6]
            self.okres_nazev = row[7]
            self.kraj_kod = row[8]
            self.vusc_kod = row[9]
            self.pou_nazev = row[10]
            self.orp_kod = int(row[11])
            self.kraj_nazev = row[12]
            self.stat_kod = row[13]
            self.vusc_nazev = row[14]
            self.regionsoudrznosti_kod = row[15]
            self.vusc_nutslau = row[16]
            self.orp_nazev = row[17]
            self.stat_nazev = row[18]
            self.stat_nutslau = row[19]
            self.regionsoudrznosti_nazev = row[20]
            self.regionsoudrznosti_nutslau = row[21]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


class Zsj:
    # Zakladni sidelni jednotka
    id: int
    nazev: str
    ku_kod: int
    ku_nazev: str
    obec_kod: int
    obec_nazev: str
    obec_statuskod: int
    okres_kod: int
    pou_kod: int
    okres_nazev: str
    kraj_kod: int
    vusc_kod: int
    pou_nazev: str
    orp_kod: int
    kraj_nazev: str
    stat_kod: int
    vusc_nazev: str
    regionsoudrznosti_kod: int
    vusc_nutslau: str
    orp_nazev: str
    stat_nazev: str
    stat_nutslau: str
    regionsoudrznosti_nazev: str
    regionsoudrznosti_nutslau: str

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.nazev = row[1]
            self.ku_kod = row[2]
            self.ku_nazev = row[3]
            self.obec_kod = row[4]
            self.obec_nazev = row[5]
            self.obec_statuskod = row[6]
            self.okres_kod = row[7]
            self.pou_kod = row[8]
            self.okres_nazev = row[9]
            self.kraj_kod = row[10]
            self.vusc_kod = row[11]
            self.pou_nazev = row[12]
            self.orp_kod = int(row[13])
            self.kraj_nazev = row[14]
            self.stat_kod = row[15]
            self.vusc_nazev = row[16]
            self.regionsoudrznosti_kod = row[17]
            self.vusc_nutslau = row[18]
            self.orp_nazev = row[19]
            self.stat_nazev = row[20]
            self.stat_nutslau = row[21]
            self.regionsoudrznosti_nazev = row[22]
            self.regionsoudrznosti_nutslau = row[23]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, ensure_ascii=False)


class AdresniBod:
    dist: float  # OO vzdalenost od bodu
    id: int  # 01 adresnimista.kod
    cislo_domovni: int  # 02 adresnimista.cislodomovni
    cislo_orientacni: int  # 03 adresnimista.cisloorientacni
    cislo_orientacni_pismeno: str  # 04 adresnimista.cisloorientacnipismeno
    psc: int  # 05 adresnimista.psc,
    cast_obce: str  # 10 castiobci.nazev,
    obec: str  # 12 obce.nazev,
    ulice: str  # 13 ulice.nazev,
    momc: str  # 14 momc.nazev,
    mop: str  # 16 mop.nazev

    def __init__(self, row: tuple):
        if row is not None:
            self.dist = row[0]
            self.id = row[1]
            self.cislo_domovni = row[2]
            self.cislo_orientacni = row[3]
            self.cislo_orientacni_pismeno = row[4]
            self.psc = row[5]
            self.cast_obce = row[10]
            self.obec = row[12]
            self.ulice = row[13]
            self.momc = row[14]
            self.mop = row[16]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, ensure_ascii=False)


class _SearchItem:
    def __init__(self, item, text, field_name):
        self.item = item
        self.text = text
        self.fieldName = field_name

    def __repr__(self):
        return self.text + " (" + self.item.value + ")"

    def get_where_item(self):
        if self.item is None:
            return ""
        else:
            return self.fieldName + "= '" + self.text + "'"

    def get_id(self):
        return self.fieldName + ':' + self.text


def none_to_string(item):
    """
    Converts item to string, unlike str or repr, None is represented as "".

    1. None is represented as "".
    2. For tuple items, tupple with values as string returned
    3. For list items, list with values as string returned

    noneToString(None) = ""
    noneToString(3) = "3"
    noneToString('3') = "3"
    noneToString((None, 3, None)) = ("", "3", "")
    noneToString([None, 3, None]) = ["", "3", ""]

    :param item: Value to be converted to string.
    :return: String representation of item, none represented as ""
    """
    if isinstance(item, tuple):
        result = ()
        for sub_item in item:
            result = result + (none_to_string(sub_item),)
        return result
    elif isinstance(item, list):
        result = []
        for sub_item in item:
            result.append(none_to_string(sub_item))
        return result
    else:
        return [str(item), ""][item is None]


def formatzip_code(code):
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
    out = ""
    if possible_number is not None:
        if str(possible_number).isdigit():
            out = str(possible_number)
    return out


def alpha_check(possible_alpha):
    out = ""
    if possible_alpha is not None and possible_alpha.isalpha():
        out = possible_alpha
    return out
