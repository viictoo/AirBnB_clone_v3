#!/usr/bin/python3
"""cities module
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_city(state_id):
    """retrieves the list of all city objects of a state

    Return:
    list of all city objects
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_object(city_id):
    """Retrieves a city object

    Returns:
    A city object given the id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object

    Args:
        city_id (str): city id

    Returns:
    an empty dictionary with the status code 200
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """Creates a city

    Returns:
    new City with the status code 201
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        return abort(400, "Missing name")

    city = City(**request.get_json())
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """Updates a city object

    Args:
        city_id (str): city id

    Returns:
    City object with the status code 200
    """
    city = storage.get(City, city_id)
    if not city:
        abort(400)
    # request_body = request.get_json()
    if not request.get_json():
        abort(400, "Not a JSON")
    request_body = request.get_json()
    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and\
                key != 'updated_at' and key != 'state_id':
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
