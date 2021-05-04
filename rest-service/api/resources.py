# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         resources
# Purpose:      resources used in the REST API
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
import json

from flask import Response, request
from flask_restful import Resource, abort, reqparse

from service.conversion import point2wgs, point2jtsk, string_wgs_to_jtsk
from service.models import Coordinates, CoordinatesGps
from service.geolocation_reverse import get_maplist, get_ku, get_parcela, get_povodi, get_zsj

__author__ = 'SYSNET'


def illegal_method(method):
    abort(404, message="Metoda {} není podporována ".format(method))


def missing_arguments():
    abort(404, message="Chybí argumenty ")


def to_json(o):
    return json.dumps(o, default=lambda obj: o.__dict__)


parser = reqparse.RequestParser()
parser.add_argument('x', type=float, help='Souřadnice X geolokace')
parser.add_argument('y', type=float, help='Souřadnice y geolokace')
parser.add_argument('lat', type=str, help='Zeměpisná šířka geolokace')
parser.add_argument('lon', type=str, help='Zeměpisná délka geolokace')


# ParcelaApi: returns Parcela from RUIAN
class ParcelaApi(Resource):
    def get(self):
        return _doit_parcela(_parse_coordinates_get())

    def post(self):
        return _doit_parcela(_parse_coordinates())


# ZsjApi: returns Zsj from RUIAN
class ZsjApi(Resource):
    def get(self):
        return _doit_zsj(_parse_coordinates_get())

    def post(self):
        return _doit_zsj(_parse_coordinates())


# KujApi: returns katastralniUzemi from RUIAN
class KuApi(Resource):
    def get(self):
        return _doit_ku(_parse_coordinates_get())

    def post(self):
        return _doit_ku(_parse_coordinates())


# RozvodniceApi: returns Rozvodnice from POVODI
class RozvodniceApi(Resource):
    def get(self):
        return _doit_rozvodnice(_parse_coordinates_get())

    def post(self):
        return _doit_rozvodnice(_parse_coordinates())


# MaplistApi: returns MapovyList50 from MAPY
class MaplistApi(Resource):
    def get(self):
        return _doit_maplist(_parse_coordinates_get())

    def post(self):
        return _doit_maplist(_parse_coordinates())


# PointToJtskApi: converts point WGS84 (4326) to JTSK (5514)
class PointToJtskApi(Resource):
    def get(self):
        return _doit_point2jtsk(_parse_coordinates_wgs_get())

    def post(self):
        return _doit_point2jtsk(_parse_coordinates_wgs())


# PointToWgsApi: converts point JTSK (5514) to WGS84 (4326)
class PointToWgsApi(Resource):
    def get(self):
        return _doit_point2wgs(_parse_coordinates_get())

    def post(self):
        return _doit_point2wgs(_parse_coordinates())


# NearestApi: returns NearestAdresses from RUIAN
# TODO
class NearestApi(Resource):
    def get(self):
        illegal_method('GET')

    def post(self):
        args = parser.parse_args()
        geo = Coordinates(x=args['x'], y=args['y'])
        parc = get_parcela(geo.y, geo.x)
        if parc is None:
            err = {"error": "Geolocation not found", "x": geo.x, "y": geo.y}
            return Response(json.dumps(err), mimetype='application/json')
        return Response(json.dumps(parc.__dict__), mimetype='application/json')


def _doit_parcela(geo):
    if geo is None:
        missing_arguments()
    item = get_parcela(geo.y, geo.x)
    return _response(geo, item)


def _doit_zsj(geo):
    if geo is None:
        missing_arguments()
    item = get_zsj(geo.y, geo.x)
    return _response(geo, item)


def _doit_ku(geo):
    if geo is None:
        missing_arguments()
    item = get_ku(geo.y, geo.x)
    return _response(geo, item)


def _doit_rozvodnice(geo):
    if geo is None:
        missing_arguments()
    item = get_povodi(geo.y, geo.x)
    return _response(geo, item)


def _doit_maplist(geo):
    if geo is None:
        missing_arguments()
    item = get_maplist(geo.y, geo.x)
    return _response(geo, item)


def _doit_point2wgs(geo):
    if geo is None:
        missing_arguments()
    item = point2wgs(y=geo.y, x=geo.x)
    return _response(geo, item)


def _doit_point2jtsk(geo):
    if geo is None:
        missing_arguments()
    item = point2jtsk(lat=geo.lat, lon=geo.lon)
    return _response_wgs(geo, item)


def _response(geo, item):
    if item is None:
        err = {"error": "Geolocation not found", "x": geo.x, "y": geo.y}
        return Response(json.dumps(err), mimetype='application/json')
    return Response(json.dumps(item.__dict__), mimetype='application/json')


def _response_wgs(geo, item):
    if item is None:
        err = {"error": "Geolocation not found", "lat": geo.lat, "lon": geo.lon}
        return Response(json.dumps(err), mimetype='application/json')
    return Response(json.dumps(item.__dict__), mimetype='application/json')


def _parse_coordinates():
    out = None
    args = parser.parse_args()
    if args is None:
        return None
    if ('x' in args) and ('y' in args):
        out = Coordinates(x=args['x'], y=args['y'])
    elif ('lat' in args) and ('lon' in args):
        s = args['lat'] + ', ' + args['lon']
        jtsk = string_wgs_to_jtsk(str)
        if jtsk is not None:
            out = Coordinates(x=jtsk.x, y=jtsk.y)
    return out


def _parse_coordinates_wgs():
    args = parser.parse_args()
    if args is None:
        return None
    if 'lat' not in args:
        return None
    if 'lon' not in args:
        return None
    out = CoordinatesGps(lat=args['lat'], lon=args['lon'])
    return out


def _parse_coordinates_get():
    args = request.args
    out = None
    if ('x' in args) and ('y' in args):
        x = args['x']
        y = args['y']
        out = Coordinates(x=float(x), y=float(y))
    elif ('lat' in args) and ('lon' in args):
        lat = args['lat']
        lon = args['lon']
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = Coordinates(x=jtsk.x, y=jtsk.y)
    return out


def _parse_coordinates_wgs_get():
    args = request.args
    lat = args['lat']
    lon = args['lon']
    out = None
    if not (lat is None) and not (lon is None):
        out = CoordinatesGps(lat=float(lat), lon=float(lon))
    return out
