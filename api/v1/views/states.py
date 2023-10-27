#!/usr/bin/python3
"""states module
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """retrieves the list of all state objects

    Return:
    list of all state objects
    """
    all_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in all_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_object(state_id):
    """Retrieves a state object

    Returns:
    A state object given the id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object

    Args:
        state_id (str): state id

    Returns:
    an empty dictionary with the status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """Creates a state

    Returns:
    new State with the status code 201
    """
    if not request.get_json():
        return abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        return abort(400, description="Missing name")
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """Updates a state object

    Args:
        state_id (str): state id

    Returns:
    State object with the status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    request_body = request.get_json()
    if not request_body:
        abort(400, description="Not a JSON")
    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
