#!/usr/bin/python3
""" app module"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(err):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """handle errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """entry point
    """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
