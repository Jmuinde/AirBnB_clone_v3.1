#!/usr/bin/python3
""" Script to create endpoints associated with State class"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
	""" Retrives states objects"""
	state_obj = storage.all(State)
	return jsonify([obj.to_dict() for obj in state_obj.values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
	""" Retrives a state object based on its I.D"""
	state_obj = storage.get(State, state_id)
	if not state_obj:
		abort(404, 'Not found')
	return jsonify(state_obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
	"""Deletes a state object based on its i.d"""
	state_obj = storage.get(State, state_id)
	if not state_obj:
		abort(404, 'Not Found')
	state_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
	"""creates/adds a new state object into the database"""
	new_state = request.get_json()
	if not new_state:
		abort(400, 'Not a Json')
	if 'name' not in new_state:
		abort(400, "Missing name")
	obj = State(**new_state)
	storage.new(obj)
	storage.save()
	return jsonify(obj.to_dict(), 201)

@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
	"""Update a state object based on its id"""
	state_obj = storage.get(State, state_id)
	if not state_obj:
		abort(404, 'Not found')
	update_state = request.get_json()
	if not update_state:
		abort(400, "Not a JSON")
	for key, value in update_state.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(state_obj, key, value)
	storage.save()
	return make_response(jsonify(state_obj.to_dict()), 200)
