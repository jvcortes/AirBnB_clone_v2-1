#!/usr/bin/python3
"""
Starts the Flask web API.
"""
import os
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def db_close(exc):
    """ Closes the database connection. """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ A handler for 404 errors """
    return make_response(jsonify({
        "error": "Not found"
    }), 404)

if __name__ == '__main__':
    port = 5000
    host = "0.0.0.0"
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')

    app.run(host, port, threaded=True)
