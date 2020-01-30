#!/usr/bin/python3
"""
Defines the API States endpoint.
"""
from flask import jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states')
def states():
    """
    Lists all the State instances.
    """
    all_states = [State.to_dict(obj) for obj in
                  storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<id>', methods=['GET'])
def get(id):
    """
    Gets a State instance by its ID. If no State is found, the function will
    return a 404 response.

    Arguments:
        id (str): State
    """
    state = storage.get("State", id).to_dict()
    if not state:
        return "Not found", 404
    return jsonify(state)


@app_views.route('/states', methods=['POST'])
def create():
    """
    Creates a State instance.

    If the JSON doesn't contain a "name" entry, the function will return
    a 400 response.

    If the request contains an invalid JSON, the function will return a
    400 response.
    """
    attributes = request.get_json()
    if not attributes:
        return "Not a JSON", 400

    if "name" not in attributes:
        return "Missing name", 400

    state = State(**attributes)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def update(id):
    """
    Updates a State instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no state is found, the function will return a 404 response.
    """
    attributes = request.get_json()
    if not attributes:
        return "Not a JSON", 400

    attributes.pop("id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    state = storage.get("State", id)
    if not state:
        return "Not found", 404

    for name in attributes:
        setattr(state, name, attributes[name])
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<id>', methods=['DELETE'])
def delete(id):
    """
    Deletes a State instance.

    If no state is found, the function will return a 404 response.
    """
    state = storage.get("State", id)
    if not state:
        return "Not found", 404

    state.delete()
    return jsonify('{}'), 200
