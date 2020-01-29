#!/usr/bin/python3
"""
Defines the index for V1 API.
"""
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
import models


@app_views.route('/status')
def status():
    """
    Returns OK
    """
    return make_response(jsonify({
        'status': "OK"
    }))


@app_views.route('/stats')
def retrieve_number():
    """
    Endpoint that retrieves the number of each objects by type
    """
    return make_response(jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }))
