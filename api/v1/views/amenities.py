#!/usr/bin/python3
""" Script to create endpoints associated with Amenity class"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
	""" Retrives the list of amenity object in the db"""
	amenity_obj = storage.all(Amenity)
	return jsonify([obj.to_dict() for obj in amenity_obj.values()])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
	"""Retrivies an amenity object based on its i.d"""
	amenity_obj = storage.get(Amenity, amenity_id)
	if not amenity_obj:
		abort(404, 'Not found')
	return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
	""" Deletes an amenity object based on its i.d"""
	amenity_obj = storage.get(Amenity, amenity_id)
	if not amenity_obj:
		abort(404, 'Not Found')
	amenity_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
	"""creates/adds a new amenity object and adds it to the db"""
	new_amenity = request.get_json()
	if not new_amenity:
		abort(400, 'Not a Json')
	if 'name' not in new_amenity:
		abort(400, "Missing name")
	amenity_obj = Amenity(**new_amenity)
	storage.new(amenity_obj)
	storage.save()
	return jsonify(amenity_obj.to_dict(), 201)

@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
	""" Updates an amenity object based on its id"""
	amenity_obj = storage.get(Amenity, amenity_id)
	if not amenity_obj:
		abort(404, 'Not found')
	update_amenity = request.get_json()
	if not update_amenity:
		abort(400, "Not a JSON")
	for key, value in update_amenity.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(amenity_obj, key, value)
	storage.save()
	return make_response(jsonify(amenity_obj.to_dict()), 200)
