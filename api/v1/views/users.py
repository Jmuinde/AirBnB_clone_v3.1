#!/usr/bin/python3
""" Script to create endpoints associated with User class"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
	""" Retrives the list of User objects in the db"""
	user_obj = storage.all(User)
	return jsonify([obj.to_dict() for obj in user_obj.values()])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
	"""Retrivies an amenity object based on its i.d"""
	user_obj = storage.get(User, user_id)
	if not user_obj:
		abort(404, 'Not found')
	return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
	""" Deletes a user object based on its i.d"""
	user_obj = storage.get(User, user_id)
	if not user_obj:
		abort(404, 'Not Found')
	user_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
	"""creates/adds a new user object and adds it to the db"""
	new_user = request.get_json()
	if not new_user:
		abort(400, 'Not a Json')
	if 'email' not in new_user:
		abort(400, 'Missing email')
	if 'password' not in new_user:
		abort(400, 'Missing password')

	user_obj = User(**new_user)
	storage.new(user_obj)
	storage.save()
	return jsonify(user_obj.to_dict(), 201)

@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
	""" Updates a user object based on its id"""
	user_obj = storage.get(User, user_id)
	if not user_obj:
		abort(404, 'Not found')
	update_user = request.get_json()
	if not update_user:
		abort(400, "Not a JSON")
	for key, value in update_user.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(user_obj, key, value)
	storage.save()
	return make_response(jsonify(user_obj.to_dict()), 200)
