#!/usr/bin/python3

"""
Defines the API Users endpoint
"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def users():
    """
    Lists all the User instances.
    """
    all_users = [User.to_dict(user) for user in storage.all("User").values()]
    return jsonify(all_users)


@app_views.route('/users/<id>', methods=['GET'])
def get_user(id):
    """
    Gets a User instance by its ID. If no User is found, the function will
    return a 404 response.

    Arguments:
        id (str): User ID
    """
    user = storage.get("User", id)
    if not user:
        abort(404, "Not found")
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a User instance.

    If the JSON doesn't contain a "email" or "password" entry, the function
    will return a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.

    Arguments:
        id (str): User ID
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    if "email" not in attributes:
        abort(400, "Missing email")

    if "password" not in attributes:
        abort(400, "Missing password")

    user = User(**attributes)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<id>', methods=['PUT'])
def update_user(id):
    """
    Updates a User instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no user is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("id", None)
    attributes.pop("email", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    user = storage.get("User", id)
    if not user:
        abort(404, "Not found")

    for name in attributes:
        setattr(user, name, attributes[name])
    user.save()

    return jsonify(user.to_dict()), 200


@app_views.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Deletes a User instance.

    If no user is found, the function will return a 404 response.
    """
    user = storage.get("User", id)
    if not user:
        abort(404, "Not found")

    user.delete()
    storage.save()

    return jsonify({}), 200
