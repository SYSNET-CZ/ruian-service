import json

from flask import Flask, Response, redirect, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from service.ruian_connection import get_parcela, get_rozvodnice

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)


TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


class GeolocationDao(dict, object):
    geo_id: str
    x: float
    y: float

    def __init__(self, geo_id, x, y):
        dict.__init__(self, geo_id=geo_id, x=x, y=y)
        self.geo_id = geo_id
        self.x = x
        self.y = y

        # This field will not be sent in the response
        self.status = 'active'


GEOLOCATIONS = {
    'geo1': GeolocationDao(geo_id="geo1", x=446.456, y=789.145),
    'geo2': GeolocationDao(geo_id="geo2", x=1234.45, y=74.7895),
    'geo3': GeolocationDao(geo_id="geo3", x=15.8, y=745.8)
}


def to_json(o):
    return json.dumps(o, default=lambda obj: o.__dict__)


def illegal_method(method):
    abort(404, message="Metoda {} není podporována ".format(method))


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


def abort_if_geolocation_doesnt_exist(geo_id):
    if geo_id not in GEOLOCATIONS:
        abort(404, message="Geolocation {} doesn't exist".format(geo_id))


parser = reqparse.RequestParser()
parser.add_argument('task', type=str, help='Testovací task')
parser.add_argument('x', type=float, help='Souřadnice X geolokace')
parser.add_argument('y', type=float, help='Souřadnice y geolokace')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


geo_fields = {
    'geo_id': fields.String,
    'x': fields.Float,
    'y': fields.Float
}


# Geolocation
# shows a single Geolocation item and lets you delete a Geolocation item
class Geolocation(Resource):
    @marshal_with(geo_fields)
    def get(self, geo_id):
        abort_if_geolocation_doesnt_exist(geo_id)
        out = GEOLOCATIONS[geo_id]
        return out

    def delete(self, geo_id):
        abort_if_geolocation_doesnt_exist(geo_id)
        del GEOLOCATIONS[geo_id]
        return '', 204

    def put(self, geo_id):
        args = parser.parse_args()
        # geo = {'x': args['x'], 'y': args['y']}
        geo = GeolocationDao(geo_id=geo_id, x=args['x'], y=args['y'])
        GEOLOCATIONS[geo_id] = geo
        return geo, 201


# GeolocationList
# shows a list of all geolocations, and lets you POST to add new tasks
class GeolocationList(Resource):
    def get(self):
        return GEOLOCATIONS

    def post(self):
        args = parser.parse_args()
        geo_id = int(max(GEOLOCATIONS.keys()).lstrip('geo')) + 1
        geo_id = 'geo%i' % geo_id
        geo = GeolocationDao(geo_id=geo_id, x=args['x'], y=args['y'])
        # GEOLOCATIONS[geo_id] = {'x': args['x'], 'y': args['y']}
        GEOLOCATIONS[geo_id] = geo
        # return GEOLOCATIONS[geo_id], 201
        return geo, 201


# ParcelaApi
# returns Parcela from RUIAN
class ParcelaApi(Resource):
    def get(self):
        illegal_method('GET')

    def post(self):
        args = parser.parse_args()
        geo_id = int(max(GEOLOCATIONS.keys()).lstrip('geo')) + 1
        geo_id = 'geo%i' % geo_id
        geo = GeolocationDao(geo_id=geo_id, x=args['x'], y=args['y'])
        # GEOLOCATIONS[geo_id] = {'x': args['x'], 'y': args['y']}
        GEOLOCATIONS[geo_id] = geo
        parc = get_parcela(geo.y, geo.x)
        if parc is None:
            err = {"error": "Geolocation not found", "x": geo.x, "y": geo.y}
            return Response(json.dumps(err), mimetype='application/json')
        return Response(json.dumps(parc.__dict__), mimetype='application/json')


# RozvodniceApi
# returns Rozvodnice from RUIAN
class RozvodniceApi(Resource):
    def get(self):
        illegal_method('GET')

    def post(self):
        args = parser.parse_args()
        geo_id = int(max(GEOLOCATIONS.keys()).lstrip('geo')) + 1
        geo_id = 'geo%i' % geo_id
        geo = GeolocationDao(geo_id=geo_id, x=args['x'], y=args['y'])
        # GEOLOCATIONS[geo_id] = {'x': args['x'], 'y': args['y']}
        GEOLOCATIONS[geo_id] = geo
        rozv = get_rozvodnice(geo.y, geo.x)
        if rozv is None:
            err = {"error": "Geolocation not found", "x": geo.x, "y": geo.y}
            return Response(json.dumps(err), mimetype='application/json')
        return Response(json.dumps(rozv.__dict__), mimetype='application/json')


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(GeolocationList, '/geolocations')
api.add_resource(Geolocation, '/geolocations/<geo_id>')
api.add_resource(ParcelaApi, '/geoapi/parcela', '/geoapi/parcela/', endpoint="geoapi")
api.add_resource(RozvodniceApi, '/geoapi/rozvodnice', '/geoapi/rozvodnice/', endpoint="geoapi")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
