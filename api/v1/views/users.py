#!/usr/bin/python3
"""users module
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_get():
    """Retrieves the list of all User objects

    Returns:
        all User objects
    """
    all_users = storage.all(User)
    return jsonify([obj.to_dict() for obj in all_users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_object(user_id):
    """Retrieves a user object

    Returns:
    A user object given the id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object

    Args:
        user_id (str): user id

    Returns:
    an empty dictionary with the status code 200
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Creates a user

    Returns:
    new user with the status code 201
    """
    if not request.get_json():
        return abort(400, "Not a JSON")
    if 'email' not in request.get_json():
        return abort(400, "Missing email")
    if 'password' not in request.get_json():
        return abort(400, "Missing password")
    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """Updates a user object

    Args:
        user_id (str): user id

    Returns:
    User object with the status code 200
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and\
                key != 'updated_at' and key != 'email':
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
