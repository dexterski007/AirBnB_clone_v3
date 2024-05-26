#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """ route for status """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ route to count the number of objects in storage """
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return jsonify(stats)
