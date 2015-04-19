from app import application, cm
import logging
from flask import request, Response, jsonify
import json
from boto.dynamodb2.table import Table
import base64

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from lib.helpers.map import Geocode



# Home page
@application.route('/', methods=["PUT", "POST"])
def index():
	response = None
	decoded = base64.b64decode(request.get_data())
	test_table = Table('test', connection=cm.db)
	test_table.put_item(data={
		"id": "worker" + sha1(str(datetime.now())).hexdigest(),
		"data": decoded
	})
	response = Response("OK!", status=200)
	return response

@application.route('/add', methods=["PUT", "POST"])
def add():
	# Get the data
	data = json.loads(request.get_data())

	current_time = data.get("current_time")
	schedule = data.get("data")

	# Check if the type is valid
	if current_time is None or schedule is None or not isinstance(schedule, list):
		response = Response("Ignoring", status=200)
		response.headers['Access-Control-Allow-Origin'] = '*';
		return response

	geocode = Geocode()

	# Get each stop in the request
	for stop in schedule:
		stop["stop_id"] = geocode.get_place(stop["lat"], stop["lon"])
	
	print schedule
	response = Response(stop, status=200)
	response.headers['Access-Control-Allow-Origin'] = '*';
	return response

@application.route('/test', methods=["GET"])
def rest():
	geocode = Geocode()
	return str(geocode.get_place(lat=11.9838736,lon=75.5545614))

