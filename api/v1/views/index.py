#!/usr/bin/python3
"""
Defines the index for V1 API.
"""
import json
from flask import Response
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    Returns OK
    """
    return Response(json.dumps({'status': "OK"}, indent=2),
                    mimetype='application/json')
