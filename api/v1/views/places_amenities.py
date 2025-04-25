#!/usr/bin/python3
""" Script to create view link between place and Amenity
to handle all default API calls
"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def amenity_by_place(place_id):
	"""Retrives the list of all Amenity objects of a place"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not found')

	if getenv('HBNB_TYPE_STORAGE') == 'db':
		obj = [obj.to_dict() for obj in place_obj.amenities]
	else:
		obj = [storage.get(Amenity, amenity_id).tod_dict()
				for amenity_id in place_obj.amenity_ids]
	return jsonify(obj)

"""@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
	Retrivies a place object based on its i.d
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not found')
	return jsonify(place_obj.to_dict())"""


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
	"""Deletes amenity obj in a place"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not Found')
	amenity_obj = storage.get(Amenity, amenity_id)
	if not amenity_obj:
		abort(404, 'Not Found')
	for obj in place_obj.amenities:
		if obj.id == amenity_obj:
			if getenv('HBNB_TYPE_Storage') == 'db':
				place_obj.amenities.remove(amenity_obj)
		else:
			place_obj.amenity_id.remove(amenity_obj)
		storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', 
				methods =['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
	"""Links an amenity object to a place"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Place not found')
	amenity_obj = storage.get(Amenity, amenity_id)
	if not amenity_id:
		abort(404, 'Amenity not found')

	if getenv('HBNB_TYPE_STORAGE') == 'db':
		if amenity_obj in place_obj.amenities:
			return jsonify(amenity_obj.to_dict(), 200)
		place_obj.amenities.append(amenity_obj)
	else:
		if amenity_id in place_obj.amenity_ids:
			return jsonify(amenity_obj.to_dict(), 200)
		place_obj.amenity_ids.append(amenity_id)
	storage.save()
	return jsonify(amenity_obj.to_dict(), 201)	
			

"""@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
	creates/adds a new place object in relation to a city
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
	Update a place object based on its id
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
	return make_response(jsonify(place_obj.to_dict()), 200)"""
