#!/usr/bin/python3
"""
Defines the API States endpoint.
"""
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """
    Lists all the Amenity instances.
    """
    all_amenities = [Amenity.to_dict(obj) for obj in
                     storage.all("Amenity").values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Gets a Amenity instance by its ID. If no Amenity is found,
    the function will return a 404 response.

    Arguments:
        id (str): Amenity
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Creates a Amenity instance.

    If the JSON doesn't contain a "name" entry, the function will return
    a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    if "name" not in attributes:
        abort(400, "Missing name")

    amenity = Amenity(**attributes)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates a Amenity instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no amenity is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("amenity_id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")

    for name in attributes:
        setattr(amenity, name, attributes[name])
    amenity.save()

    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a Amenity instance.

    If no amenity is found, the function will return a 404 response.
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")

    amenity.delete()
    storage.save()

    return jsonify({}), 200
