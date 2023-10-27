#!/usr/bin/python3
""" handles all default RESTFul API actions for Amenities class"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def all_place_amens(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_all = []
    if getenv('HBNB_TYPE_STORAGE') == "db":
        for amen in place.amenities:
            list_all.append(amen.to_dict())
    else:
        for amen in place.amenity_ids:
            list_all.append(storage.get(Amenity, amen).to_dict())
    return jsonify(list_all)

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amens(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amen = storage.get(Amenity, amenity_id)
    if not amen:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amen not in place.amenities:
            abort(404)
        place.amenities.remove(amen)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_place_amens(place_id, amenity_id):
    """ Link a Amenity object to a Place """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amen = storage.get(Amenity, amenity_id)
    if not amen:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amen in place.amenities:
            return jsonify(amen.to_dict()), 200
        else:
            place.amenities.append(amen)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amen.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amen.to_dict()), 201
