#!/usr/bin/python3
"""
Defines the index for V1 API.
"""
import json
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    Returns OK
    """
    return json.dumps({'status': "OK"}, indent=2)
