#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """ route to retrieve all amenities """
    amenities_list = storage.all(Amenity).values()
    amenities_json = []
    for amenity in amenities_list:
        amenities_json.append(amenity.to_dict())

    return jsonify(amenities_json)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenities_get(amenity_id=None):
    """ route to retrieve specific Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenities_del(amenity_id):
    """ route to delete specific Amenity """
    Amenity_todel = storage.get(Amenity, amenity_id)
    if Amenity_todel is None:
        abort(404)
    storage.delete(Amenity_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenities_p():
    """ route to post new Amenity """
    Amenity_imp = request.get_json(force=True, silent=True)
    if not Amenity_imp:
        abort(400, "Not a JSON")
    if "name" not in Amenity_imp:
        abort(400, "Missing name")
    Amenity_new = Amenity(**Amenity_imp)
    Amenity_new.save()
    return jsonify(Amenity_new.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """ edit a specific Amenity """
    to_upd = storage.get(Amenity, amenity_id)
    if to_upd is None:
        abort(404)
    Amenity_imp = request.get_json(force=True, silent=True)
    if not Amenity_imp:
        abort(400, "Not a JSON")
    to_upd.name = Amenity_imp.get("name", to_upd.name)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
