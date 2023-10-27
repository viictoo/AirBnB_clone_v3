#!/usr/bin/python3
""" handles all default RESTFul API actions for Amenities class"""
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_place(city_id):
    """ list of all objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    list_all = []
    for place in city.places:
        list_all.append(place.to_dict())
    return jsonify(list_all)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a City object: """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """ deletes an Instance of a Class """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ adds object from POST data """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    if 'name' not in obj:
        abort(400, description='Missing name')
    if 'user_id' not in obj:
        abort(400, description='Missing user_id')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user = storage.get(User, obj.get('user_id'))
    if not user:
        abort(404)

    obj['city_id'] = city_id
    instance = Place(**obj)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object using PUT """
    obj = request.get_json()
    if not obj:
        abort(400, description='Not a JSON')
    instance = storage.get(Place, place_id)
    if not instance:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in obj.items():
        if key not in ignore:
            setattr(instance, key, value)
    storage.save()
    return jsonify(instance.to_dict()), 200


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
