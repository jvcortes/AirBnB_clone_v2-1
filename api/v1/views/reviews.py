#!/usr/bin/python3
"""
Defines the API Reviews endpoint.
"""
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews(place_id):
    """
    Lists all the Review instances by a place. If no place is found,
    the function will return a 404 response.

    Arguments:
        place_id: Place ID
    """
    if not storage.get("Place", place_id):
        abort(404, "Not found")

    all_reviews = list(
        filter(lambda review: review["place_id"] == place_id,
               [Review.to_dict(review) for review in
                storage.all("Review").values()]))
    return jsonify(all_reviews)


@app_views.route('/reviews/<id>', methods=['GET'])
def get_review(id):
    """
    Gets a Review instance by its ID. If no place is found, the function will
    return a 404 response.

    Arguments:
        id (str): Review ID
    """
    review = storage.get("Review", id)
    if not review:
        abort(404, "Not found")
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_place(place_id):
    """
    Creates a Review instance.

    If the JSON doesn't contain a "user_id" or "text" entry, the function
    will return a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.

    Arguments:
        place_id (str): Place ID
    """
    if not storage.get("Place", place_id):
        abort(404, "Not found")

    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    if "user_id" not in attributes:
        abort(400, "Missing user_id")

    if "text" not in attributes:
        abort(400, "Missing text")

    attributes["place_id"] = place_id
    review = Review(**attributes)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<id>', methods=['PUT'])
def update_review(id):
    """
    Updates a Review instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no review is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("id", None)
    attributes.pop("user_id", None)
    attributes.pop("place_id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    review = storage.get("Review", id)
    if not review:
        abort(404, "Not found")

    for name in attributes:
        setattr(review, name, attributes[name])
    review.save()

    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<id>', methods=['DELETE'])
def delete_review(id):
    """
    Deletes a Review instance.

    If no place is found, the function will return a 404 response.
    """
    review = storage.get("Review", id)
    if not review:
        abort(404, "Not found")

    review.delete()
    storage.save()

    return jsonify({}), 200
