#!/usr/bin/python3
""" handles all default RESTFul API actions for Review class"""
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ list of all objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_all = []
    for review in place.reviews:
        list_all.append(review.to_dict())
    return jsonify(list_all)


@app_views.route('/reviews/<id>',
                 methods=['GET'], strict_slashes=False)
def get_review(id):
    """ Retrieves a Review instance: """
    obj = storage.get(Review, id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(id):
    """ deletes an Instance of a Class """
    obj = storage.get(Review, id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(id):
    """ adds object from POST data """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    if 'text' not in obj:
        abort(400, description='Missing text')
    if 'user_id' not in obj:
        abort(400, description='Missing user_id')

    place = storage.get(Place, id)
    if not place:
        abort(404)
    user = storage.get(User, obj.get('user_id'))
    if not user:
        abort(404)

    obj['place_id'] = id
    instance = Review(**obj)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/reviews/<id>',
                 methods=['PUT'], strict_slashes=False)
def update_reviews(id):
    """ Updates a review object using PUT """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    instance = storage.get(Review, id)
    if not instance:
        abort(404)

    ignor = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in obj.items():
        if key not in ignor:
            setattr(instance, key, value)
    storage.save()
    return jsonify(instance.to_dict()), 200
