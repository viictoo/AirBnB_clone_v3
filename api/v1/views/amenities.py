#!/usr/bin/python3
""" handles all default RESTFul API actions for Amenities class"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, Response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """ list of all Amenity objects """
    amenity_values = storage.all(Amenity).values()
    list_all = []
    for amenity in amenity_values:
        list_all.append(amenity.to_dict())
    return jsonify(list_all)


@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def one_amenity(amenity_id):
    """ Retrieves a Amenity object: """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>/',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """ Retrieves a Amenity object: """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    """ adds amenity object from POST data """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    if 'name' not in obj:
        abort(400, description='Missing name')

    instance = Amenity(**obj)

    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object using PUT """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    instance = storage.get(Amenity, amenity_id)
    if not instance:
        abort(404)

    for key, value in obj.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(instance, key, value)
    storage.save()
    return jsonify(instance.to_dict()), 200
