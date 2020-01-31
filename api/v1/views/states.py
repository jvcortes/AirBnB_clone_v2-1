#!/usr/bin/python3
"""
Defines the API States endpoint.
"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def states():
    """
    Lists all the State instances.
    """
    all_states = [State.to_dict(obj) for obj in
                  storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<id>', methods=['GET'])
def get_state(id):
    """
    Gets a State instance by its ID. If no State is found, the function will
    return a 404 response.

    Arguments:
        id (str): state ID
    """
    state = storage.get("State", id)
    if not state:
        abort(404, "Not found")
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Creates a State instance.

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

    state = State(**attributes)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def update_state(id):
    """
    Updates a State instance.

    If the request contains an invalid JSON, the function will return a
    400 response.

    If no state is found, the function will return a 404 response.

    Arguments:
        id (str): state ID
    """
    attributes = request.get_json()
    if not attributes:
        abort(400, "Not a JSON")

    attributes.pop("id", None)
    attributes.pop("created_at", None)
    attributes.pop("updated_at", None)

    state = storage.get("State", id)
    if not state:
        abort(404, "Not found")

    for name in attributes:
        setattr(state, name, attributes[name])
    state.save()

    return jsonify(state.to_dict()), 200


@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """
    Deletes a State instance.

    If no state is found, the function will return a 404 response.

    Arguments:
        id (str): state ID
    """
    state = storage.get("State", id)
    if not state:
        abort(404, "Not found")

    state.delete()
    storage.save()

    return jsonify({}), 200
