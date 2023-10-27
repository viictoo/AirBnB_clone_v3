#!/usr/bin/python3
""" index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_ok():
    """return status JSON"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stor_count():
    """return number of each objects by type: """
    count = {
            'amenities': storage.count("Amenity"),
            'cities': storage.count("City"),
            'places': storage.count("Place"),
            'reviews': storage.count("Review"),
            'states': storage.count("State"),
            'users': storage.count("User")
            }
    return jsonify(count)
