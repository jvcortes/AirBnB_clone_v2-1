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
    all_states = [State.to_dict(obj) for obj in
                  storage.all("State").values()]
    return jsonify(all_states)


@app_views.route('/states/<id>', methods=['GET'])
def get(id):
    state = storage.get("State", id).to_dict()
    if not state:
        return "Not found", 404
    return jsonify(state)


@app_views.route('/states', methods=['POST'])
def create(id):
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
    state = storage.get("State", id)
    if not state:
        return "Not found", 404

    state.delete()
    return jsonify('{}'), 200
