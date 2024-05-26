#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """ route to retrieve all users """
    users_list = storage.all(User).values()
    users_json = []
    for user in users_list:
        users_json.append(user.to_dict())

    return jsonify(users_json)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def users_get(user_id=None):
    """ route to retrieve specific user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def users_del(user_id):
    """ route to delete specific user """
    user_todel = storage.get(User, user_id)
    if user_todel is None:
        abort(404)
    storage.delete(user_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def users_p():
    """ route to post new user """
    user_imp = request.get_json(force=True, silent=True)
    if not user_imp:
        abort(400, "Not a JSON")
    if "email" not in user_imp:
        abort(400, "Missing email")
    if "password" not in user_imp:
        abort(400, "Missing password")
    user_new = User(**user_imp)
    user_new.save()
    return jsonify(user_new.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def users_put(user_id):
    """ edit a specific user """
    to_upd = storage.get(User, user_id)
    if to_upd is None:
        abort(404)
    user_imp = request.get_json(force=True, silent=True)
    ignored = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_imp:
        if key not in ignored:
            setattr(to_upd, key, value)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
