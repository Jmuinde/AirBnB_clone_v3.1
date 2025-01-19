#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage

# from models.state import State 

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
	""" Returns the status code in json format"""
	return jsonify(status="OK")
	
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
	"""Retrives the number of each objects type in the database"""
	return jsonify(
					amenities=storage.count('Amenity'),
					cities=storage.count('City'),
					places=storage.count('Place'),
					reviews=storage.count('Review'),
					states=storage.count('State'),
					users=storage.count('User')
					)

# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def states():
	# return jsonify(states=storage.all(State))
