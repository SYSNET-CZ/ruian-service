# -*- coding: utf-8 -*-

from service.query import _get_rozvodnice, _get_map_sheet_50, _get_administrative_division_ku, \
    _get_administrative_division_parcela, _get_administrative_division_zsj

get_povodi = _get_rozvodnice
get_maplist = _get_map_sheet_50
get_parcela = _get_administrative_division_parcela
get_zsj = _get_administrative_division_zsj
get_ku = _get_administrative_division_ku
