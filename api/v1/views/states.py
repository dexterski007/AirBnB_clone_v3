#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """ route to retrieve all states """
    states_list = storage.all(State).values()
    states_json = []
    for state in states_list:
        states_json.append(state.to_dict())

    return jsonify(states_json)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states_get(state_id=None):
    """ route to retrieve specific state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def states_del(state_id):
    """ route to delete specific state """
    state_todel = storage.get(State, state_id)
    if state_todel is None:
        abort(404)
    storage.delete(state_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def states_p():
    """ route to post new state """
    state_imp = request.get_json(force=True, silent=True)
    if not state_imp:
        abort(400, "Not a JSON")
    if "name" not in state_imp:
        abort(400, "Missing name")
    state_new = State(**state_imp)
    state_new.save()
    return jsonify(state_new.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def states_put(state_id):
    """ edit a specific state """
    to_upd = storage.get(State, state_id)
    if to_upd is None:
        abort(404)
    state_imp = request.get_json(force=True, silent=True)
    if not state_imp:
        abort(400, "Not a JSON")
    to_upd.name = state_imp.get("name", to_upd.name)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
