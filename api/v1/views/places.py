#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def getplaces(city_id):
    """ route to retrieve all places """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def places_get(place_id=None):
    """ route to retrieve specific place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_del(place_id):
    """ route to delete specific place """
    place_todel = storage.get(Place, place_id)
    if place_todel is None:
        abort(404)
    storage.delete(place_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def places_p(city_id):
    """ route to post new place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_imp = request.get_json(force=True, silent=True)
    if not place_imp:
        abort(400, "Not a JSON")
    if "name" not in place_imp:
        abort(400, "Missing name")
    if "user_id" not in place_imp:
        abort(400, "Missing user_id")
    user = storage.get(User, place_imp["user_id"])
    if user is None:
        abort(404)
    place_new = Place(city_id=city.id, **place_imp)
    place_new.save()
    return jsonify(place_new.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """ route to search place """
    search_req = request.get_json(force=True, silent=True)
    if not search_req:
        abort(400, "Not a JSON")
    states = search_req.get('states', [])
    cities = search_req.get('cities', [])
    amenities = search_req.get('amenities', [])
    
    places = set()
    if not states and not cities:
        places = set(storage.all(Place).values())
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        for place in city.places:
                            places.add(place)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    for place in city.places:
                        places.add(place)
    if amenities:
        amen_places = set()
        for place in places:
            if all(storage.get(Amenity, amenity_id) in place.amenities
                   for amenity_id in amenities):
                amen_places.add(place)
            places = amen_places
    final_places = [place.to_dict() for place in places]
    return jsonify(final_places)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def places_put(place_id):
    """ edit a specific place """
    to_upd = storage.get(Place, place_id)
    if to_upd is None:
        abort(404)
    place_imp = request.get_json(force=True, silent=True)
    if not place_imp:
        abort(400, "Not a JSON")
    to_upd.name = place_imp.get("name", to_upd.name)
    to_upd.description = place_imp.get("description", to_upd.description)
    to_upd.number_rooms = place_imp.get("number_rooms", to_upd.number_rooms)
    to_upd.number_bathrooms = place_imp.get("number_bathrooms",
                                            to_upd.number_bathrooms)
    to_upd.max_guest = place_imp.get("max_guest", to_upd.max_guest)
    to_upd.price_by_night = place_imp.get("price_by_night",
                                          to_upd.price_by_night)
    to_upd.latitude = place_imp.get("latitude", to_upd.latitude)
    to_upd.longitude = place_imp.get("longitude", to_upd.longitude)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
