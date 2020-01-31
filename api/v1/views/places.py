#!/usr/bin/python3
"""
Defines the API Places endpoint.
"""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places(city_id):
    """
    Lists all the Place instances by a city. If no city is found, the function
    will return a 404 response.

    Arguments:
        city_id: City ID
    """
    if not storage.get("City", city_id):
        abort(404, "Not found")

    all_places = list(
        filter(lambda place: place["city_id"] == city_id,
               [Place.to_dict(place) for place in
                storage.all("Place").values()]))
    return jsonify(all_places)


@app_views.route('/places/<id>', methods=['GET'])
def get_place(id):
    """
    Gets a Place instance by its ID. If no place is found, the function will
    return a 404 response.

    Arguments:
        id (str): Place ID
    """
    place = storage.get("Place", id)
    if not place:
        abort(404, "Not found")
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a Place instance.

    If the JSON doesn't contain a "name" or "user_id" entry, the function
    will return a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.

    Arguments:
        city_id (str): City ID
    """
    if not storage.get("City", city_id):
        abort(404, "Not found")

    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    if "user_id" not in attributes:
        abort(400, "Missing user_id")

    if "name" not in attributes:
        abort(400, "Missing name")

    attributes["city_id"] = city_id
    place = Place(**attributes)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<id>', methods=['PUT'])
def update_place(id):
    """
    Updates a Place instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no place is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("id", None)
    attributes.pop("user_id", None)
    attributes.pop("city_id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    place = storage.get("Place", id)
    if not place:
        abort(404, "Not found")

    for name in attributes:
        setattr(place, name, attributes[name])
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<id>', methods=['DELETE'])
def delete_place(id):
    """
    Deletes a Place instance.

    If no place is found, the function will return a 404 response.
    """
    place = storage.get("Place", id)
    if not place:
        abort(404, "Not found")

    place.delete()
    storage.save()

    return jsonify({}), 200
