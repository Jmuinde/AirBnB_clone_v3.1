#!/usr/bin/python3
""" Flask script for the project's RESTful API"""
import os
from flask import Flask, jsonify # make_response
from models import storage
from flask_cors import CORS 
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
	print(exception)
	storage.close()

@app.errorhandler(404)
def not_found(error):
	# return make_response(jsonify({'error': 'Not found'}), 404) 
	return jsonify(error='Not found'), 404

if __name__ == "__main__":
	# if host == HBNB_API_HOST:
		# host = sys.argv[2]
	# else:
		# host = '0.0.0.0'
	# if host == HBNB_API_PORT:
		# port = sys.argv[3]
	# else:
		# port = 5000
	app.run(host = '0.0.0.0', port = 5000, threaded=True, debug=True)
