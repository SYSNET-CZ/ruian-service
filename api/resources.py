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

from models import Coordinates
from geolocation_reverse import get_maplist, get_ku, get_parcela, get_povodi, get_zsj

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


# NearestApi: returns NearestAdresses from RUIAN
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


def _response(geo, item):
    if item is None:
        err = {"error": "Geolocation not found", "x": geo.x, "y": geo.y}
        return Response(json.dumps(err), mimetype='application/json')
    return Response(json.dumps(item.__dict__), mimetype='application/json')


def _parse_coordinates():
    args = parser.parse_args()
    if args is None:
        return None
    if 'x' not in args:
        return None
    if 'y' not in args:
        return None
    out = Coordinates(x=args['x'], y=args['y'])
    return out


def _parse_coordinates_get():
    args = request.args
    x = args['x']
    y = args['y']
    out = None
    if not (x is None) and not (y is None):
        out = Coordinates(x=float(x), y=float(y))
    return out
