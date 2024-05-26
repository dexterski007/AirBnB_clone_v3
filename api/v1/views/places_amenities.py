#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def getamenity(place_id):
    """ route to retrieve all amenities """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, amenity_id) for
                     amenity_id in place.amenity_id]
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def amenity_del(place_id, amenity_id):
    """ route to delete specific amenity """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenities_ids:
            abort(404)
        place.amenities_ids.remove(amenity_id)

    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def amenity_p(place_id, amenity_id):
    """ route to post new amenity """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenities_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
