#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def getcities(state_id):
    """ route to retrieve all cities """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def cities_get(city_id=None):
    """ route to retrieve specific city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_del(city_id):
    """ route to delete specific city """
    city_todel = storage.get(City, city_id)
    if city_todel is None:
        abort(404)
    storage.delete(city_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def cities_p(state_id):
    """ route to post new city """
    city_imp = request.get_json(force=True, silent=True)
    if not city_imp:
        abort(400, "Not a JSON")
    if "name" not in city_imp:
        abort(400, "Missing name")
    city_imp['state_id'] = state_id
    city_new = City(**city_imp)
    city_new.save()
    return jsonify(city_new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def cities_put(city_id):
    """ edit a specific state """
    to_upd = storage.get(City, city_id)
    if to_upd is None:
        abort(404)
    city_imp = request.get_json(force=True, silent=True)
    if not city_imp:
        abort(400, "Not a JSON")
    to_upd.name = city_imp.get("name", to_upd.name)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
