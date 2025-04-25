#!/usr/bin/python3
""" Script to create endpoints associated with the reviews class"""
from flask import jsonify, abort, make_response, request
from models import storage
# from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def review_by_place(place_id):
	"""Retrives the list of review objects of a place"""
	place_obj = storage.get(Place, place_id)
	if not place_obj:
		abort(404, 'Not found')
	return jsonify([review.to_dict() for review in place_obj.reviews])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
	""" Retrivies a review object based on its i.d"""
	review_obj = storage.get(Review, review_id)
	if not review_obj:
		abort(404, 'Not found')
	return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
	"""Deletes a review object based on its i.d"""
	review_obj = storage.get(Review, review_id)
	if not review_obj:
		abort(404, 'Not Found')
	review_obj.delete()
	storage.save()
	# return make_response(jsonify({}), 200)
	return jsonify({}, 200)

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
	"""creates/adds a new review object in relation to a place"""
	review_obj = storage.get(Place, place_id)
	if not review_obj:
		abort(404, 'Not found')
	new_review = request.get_json()
	if not new_review:
		abort(400, 'Not a Json')
	if 'user_id' not in new_review:
		abort(400, "Missing user_id")
	
	user_id = new_review['user_id']
	user_obj = storage.get(User, user_id)
	if not user_obj:
		abort(404)
	if 'text' not in new_review:
		abort(400, 'Misssing text')
	review_obj = Review(**new_review)
	setattr(review_obj, 'place_id', place_id)
	storage.new(review_obj)
	storage.save()
	return jsonify(review_obj.to_dict(), 201)

@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
	"""Update a review object based on its id"""
	review_obj = storage.get(Review, review_id)
	if not review_obj:
		abort(404, 'Not found')
	update_review = request.get_json()
	if not update_review:
		abort(400, "Not a JSON")
	for key, value in update_review.items():
		if key not in ['id', 'user_id','place_id', 'created_at', 'updated_at']:
			setattr(review_obj, key, value)
	storage.save()
	return make_response(jsonify(review_obj.to_dict()), 200)
