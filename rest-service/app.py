# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         app
# Purpose:      Main Flask REST API application
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
import os

from flask import Flask
from flask_restful import Api

from resources import RozvodniceApi, ParcelaApi, KuApi, MaplistApi, ZsjApi, PointToJtskApi, PointToWgsApi

RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "geoapi")

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)

#
# Actually setup the Api resource routing here
#
# reverzní geolokace
api.add_resource(ParcelaApi, '/' + RESOURCE_PREFIX + '/parcela')
api.add_resource(ZsjApi, '/' + RESOURCE_PREFIX + '/zsj')
api.add_resource(KuApi, '/' + RESOURCE_PREFIX + '/ku')
api.add_resource(RozvodniceApi, '/' + RESOURCE_PREFIX + '/rozvodnice')
api.add_resource(MaplistApi, '/' + RESOURCE_PREFIX + '/maplist50')

# konverze
api.add_resource(PointToJtskApi, '/' + RESOURCE_PREFIX + '/point2jtsk')
api.add_resource(PointToWgsApi, '/' + RESOURCE_PREFIX + '/point2wgs')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
