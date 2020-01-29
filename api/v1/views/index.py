#!/usr/bin/python3
"""
Defines the index for V1 API.
"""
import json
from flask import Response, jsonify
from api.v1.views import app_views
from models import storage
import models

@app_views.route('/status')
def status():
    """
    Returns OK
    """
    return Response(json.dumps({'status': "OK"}, indent=2),
                    mimetype='application/json')


@app_views.route('/stats')
def retrieveNumber():
    """
    Endpoint that retrieves the number of each objects by type
    """
    return Response(json.dumps({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }, indent=2))
