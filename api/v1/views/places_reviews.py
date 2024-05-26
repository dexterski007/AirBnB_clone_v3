#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def getreviews(place_id):
    """ route to retrieve all reviews """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def reviews_get(review_id=None):
    """ route to retrieve specific review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_del(review_id):
    """ route to delete specific review """
    review_todel = storage.get(Review, review_id)
    if review_todel is None:
        abort(404)
    storage.delete(review_todel)
    storage.save()
    empty = {}
    return jsonify(empty), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def reviews_p(place_id):
    """ route to post new review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_imp = request.get_json(force=True, silent=True)
    if not review_imp:
        abort(400, "Not a JSON")
    if "text" not in review_imp:
        abort(400, "Missing text")
    if "user_id" not in review_imp:
        abort(400, "Missing user_id")
    user = storage.get(User, review_imp["user_id"])
    if user is None:
        abort(404)
    review_new = Review(place_id=place.id, **review_imp)
    review_new.save()
    return jsonify(review_new.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def reviews_put(place_id):
    """ edit a specific review """
    to_upd = storage.get(Review, review_id)
    if to_upd is None:
        abort(404)
    review_imp = request.get_json(force=True, silent=True)
    if not review_imp:
        abort(400, "Not a JSON")
    to_upd.text = review_imp.get("text", to_upd.text)
    to_upd.save()
    return jsonify(to_upd.to_dict()), 200
