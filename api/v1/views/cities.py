#!/usr/bin/python3
"""
Defines the API States endpoint.
"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """
    Lists all the City instances by state.

    If no State instance is found, the function will return a 404 response.

    state_id (str): State ID.
    """
    if not storage.get("State", state_id):
        abort(404, "Not found")

    all_cities = list(
        filter(lambda city: city["state_id"] == state_id,
               [City.to_dict(city) for city in storage.all("City").values()]))
    return jsonify(all_cities)


@app_views.route('/cities/<id>', methods=['GET'])
def get_city(id):
    """
    Gets a City instance by its ID. If no City is found, the function will
    return a 404 response.

    Arguments:
        id (str): City ID
    """
    city = storage.get("City", id)
    if not city:
        abort(404, "Not found")
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a City instance.

    If the JSON doesn't contain a "name" entry, the function will return
    a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.

    Arguments:
        state_id (str): State ID
    """
    if not storage.get("State", state_id):
        abort(404, "Not found")

    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    if "name" not in attributes:
        abort(400, "Missing name")

    attributes["state_id"] = state_id
    city = City(**attributes)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<id>', methods=['PUT'])
def update_city(id):
    """
    Updates a City instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no city is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("id", None)
    attributes.pop("state_id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    city = storage.get("City", id)
    if not city:
        abort(404, "Not found")

    for name in attributes:
        setattr(city, name, attributes[name])
    city.save()

    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<id>', methods=['DELETE'])
def delete_city(id):
    """
    Deletes a City instance.

    If no city is found, the function will return a 404 response.
    """
    city = storage.get("City", id)
    if not city:
        abort(404, "Not found")

    city.delete()
    storage.save()

    return jsonify({}), 200
