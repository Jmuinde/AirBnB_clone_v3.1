#!/usr/bin/python3
""" Script to create endpoints associated with Place class"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views
from api.v1.views import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place_by_city(city_id):
	"""Retrives all places in selected city"""
	city_obj = storage.get(City, city_id)
	if not city_obj:
		abort(404, 'Not found')
	return jsonify([obj.to_dict() for obj in city_obj.places])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
	"""Retrivies a place object based on its i.d"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not found')
	return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
	""" Deletes a place object based on its i.d"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not Found')
	place_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
	"""creates/adds a new place object in relation to a city"""
	city_obj = storage.get(City, city_id)
	if not city_obj:
		abort(404, 'Not found')
	new_place = request.get_json()
	if not new_place:
		abort(400, 'Not a Json')
	if 'user_id' not in new_place:
		abort(400, "Missing user_id")
	
	user_id = new_place['user_id']
	user_obj = storage.get(User, user_id)
	if not user_obj:
		abort(404)
	if 'name' not in new_place:
		abort(400, 'Misssing name')
	place_obj = Place(**new_place)
	setattr(place_obj, 'city_id', city_id)
	storage.new(place_obj)
	storage.save()
	return jsonify(place_obj.to_dict(), 201)

@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
	"""Update a place object based on its id"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not found')
	update_place = request.get_json()
	if not update_place:
		abort(400, "Not a JSON")
	for key, value in update_place.items():
		if key not in ['id', 'user_id','city_id', 'created_at', 'updated_at']:
			setattr(place_obj, key, value)
	storage.save()
	return make_response(jsonify(place_obj.to_dict()), 200)
