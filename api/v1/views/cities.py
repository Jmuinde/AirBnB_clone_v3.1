#!/usr/bin/python3
""" Script to create endpoints associated with State class"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def city_by_state(state_id):
	""" Retrives all th city object related to a state"""
	state_obj = storage.get(State, state_id)
	if not state_obj:
		abort(404, 'Not found')
	return jsonify([city.to_dict() for city in state_obj.cities])

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
	"""Retrivies a city object based on its i.d"""
	city_obj = storage.get(City, city_id)
	if not city_obj:
		abort(404, 'Not found')
	return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
	"""Deletes a city object based on its i.d"""
	city_obj = storage.get(City, city_id)
	if not city_obj:
		abort(404, 'Not Found')
	city_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
	"""creates/adds a new state object in relation to a state"""
	state_obj = storage.get(State, state_id)
	if not state_obj:
		abort(404)
	new_city = request.get_json()
	if not new_city:
		abort(400, 'Not a Json')
	if 'name' not in new_city:
		abort(400, "Missing name")
	city_obj = City(**new_city)
	setattr(city_obj, 'state_id', state_id)
	storage.new(city_obj)
	storage.save()
	return jsonify(city_obj.to_dict(), 201)

@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
	"""Update a city object based on its id"""
	city_obj = storage.get(City, city_id)
	if not city_obj:
		abort(404, 'Not found')
	update_city = request.get_json()
	if not update_city:
		abort(400, "Not a JSON")
	for key, value in update_city.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(city_obj, key, value)
	storage.save()
	return make_response(jsonify(city_obj.to_dict()), 200)
