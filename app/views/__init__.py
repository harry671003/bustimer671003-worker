from app import application, cm
import logging
from flask import request, Response, jsonify
import json
import pprint

import base64

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from lib.helpers.map import Geocode
from lib.helpers.tables import tb_test, tb_schedule

from app.models.stops import get_stop
from app.models.schedules import query_schedule, update_time_centroid,\
								 get_schedule, get_schedule_info, \
								 check_schedule_existing, add_new_schedule, \
								 get_schedule_duration

from lib.helpers.time import get_xhd_from_time
from lib.helpers.algo import find_perfect_schedule
from operator import itemgetter

from lib.helpers.security import generate_128bit_id



# Home page
@application.route('/', methods=["PUT", "POST"])
def index():
	response = None
	decoded = base64.b64decode(request.get_data())
	tb_test.put_item(data={
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
	new_schedule = data.get("data")

	# Check if the type is valid
	if current_time is None or new_schedule is None or not isinstance(new_schedule, list):
		response = Response("Ignoring", status=200)
		response.headers['Access-Control-Allow-Origin'] = '*';
		return response

	geocode = Geocode()

	# find out schedules should be updated
	# Schedule counter counts the number of times stops fall in 
	# existing schedules
	schedule_counter = {}
	no_schedule_stops = []
	prominent_route_count = 0
	for stop in new_schedule:
		stop["stop_id"] = geocode.get_place(stop["lat"], stop["lon"])
		# Get the threshold and other info
		if(stop["stop_id"]):
			# Get the stop info from database
			stop_info = get_stop(stop_id=stop["stop_id"])
			# Convert the time
			time_components = stop["time"].split(":")
			hour = int(time_components[0])
			minute = int(time_components[1])
			second = int(time_components[2])

			xhd = get_xhd_from_time(hour=hour, minute=minute, second=second)
			print "xhd: " + str(xhd)
			stop["time"] = xhd
			stop["db_stop"] = stop_info
			# Now check if the stop is in the schedule table
			print stop["stop_id"]
			schedule_result = query_schedule(stop["stop_id"], stop["time"], stop_info["threshold"])
			schedule_result = list(schedule_result)
			# The current stop doesnot already exist in 
			# database schedule
			if len(schedule_result) == 0:
				no_schedule_stops.append(
					{
						"db_stop": stop_info,
						"user_stop": stop
					}
				)
			# Check for which all schedules the current stop exists
			for schedule in schedule_result:
				sch_id = schedule["sch_id"]
				print "[+] Sch ID" + sch_id
				if schedule_counter.get(sch_id):
					schedule_counter[sch_id]["stops"].append(
						{
							"db_stop": stop_info,
							"user_stop": stop
						}
					)
					schedule_counter[sch_id]["count"] += 1
				else:
					schedule_counter[sch_id] = {
						"count": 1,
						"stops": [{
							"db_stop": stop_info,
							"user_stop": stop
						}]
					}
				# Check if this count > prominent_route_count
				if schedule_counter[sch_id]["count"] > prominent_route_count:
					prominent_route_count = schedule_counter[sch_id]["count"]

	pp = pprint.PrettyPrinter(indent=4)
	print "[+] Schedule Counter: "
	pp.pprint(schedule_counter)
	print "[+] No Schedule Stops: "
	pp.pprint(no_schedule_stops)
	print "[+] prominent_route_count" + str(prominent_route_count)
	# What to do if prominent count is 1 or 
	# the number of items in schedule counter is 0
	# Make every stop part of a new route
	if prominent_route_count <= 1:
		print "[+] Entering condition, no prominent_routes"
		# Get a new sch_id
		while(1):
			sch_id = generate_128bit_id(str(stop["time"]))
			if not check_schedule_existing(sch_id):
				break
		# Add each stop to this schedule		
		for stop in new_schedule:
			print "[+ stop ]" + str(stop)
			if stop["stop_id"]:
				# This is a resolved stop
				while(1):
					s_id = generate_128bit_id(str(stop["time"]))
					if not get_schedule_info(s_id):
						add_new_schedule(
							s_id=s_id, 
							sch_id=sch_id, 
							stop_id=stop["db_stop"]["stop_id"], 
							time=stop["time"],
							num_contributors=1
						)
						break

	else:
		# There are certain prominent routes
		# So the stops has to fall in this promienent routes
		prominent_routes = []
		# find the prominent routes
		for sch_id in schedule_counter:
			if schedule_counter[sch_id]["count"] == prominent_route_count:
				# Get the start and end of prominent route
				duration = get_schedule_duration(sch_id)
				prominent_routes.append({
					"sch_id" 	: sch_id,
					"start"		: int(duration["start"]),
					"stop" 		: int(duration["stop"])
				})

		# Sort the prominent stops by start time
		# this is used in the second part of the next
		# step of the algorithm
		prominent_routes = sorted(prominent_routes, key=itemgetter('start'))

		# print "[+] prominent_routes" + str(prominent_routes)

		# Update the time of the stops in schedule_counter to the prominent route
		for sch_id in schedule_counter:
			# Check if this is a prominent route
			if any(d['sch_id'] == sch_id for d in prominent_routes):
				# This is a prominent stop
				for stop in schedule_counter[sch_id]["stops"]:
					db_stop = stop["db_stop"]
					user_stop = stop["user_stop"]

					schedule = get_schedule(
						stop_id=db_stop["stop_id"],
						sch_id=sch_id
					)

					# Get the new time and update the time centroid
					new_time = user_stop["time"]
					update_time_centroid(schedule_info=schedule, new_time=new_time)

			else:
				# This schedule is not a prominent route
				for stop in schedule_counter[sch_id]["stops"]:
					db_stop = stop["db_stop"]
					user_stop = stop["user_stop"]

					# Find to which schedule this should belong to
					perfect_sch_id = find_perfect_schedule(prominent_routes=prominent_routes, time=user_stop["time"])
					while(1):
						s_id = generate_128bit_id(perfect_sch_id)
						if not get_schedule_info(s_id):
							add_new_schedule(
								s_id=s_id, 
								sch_id=perfect_sch_id, 
								stop_id=db_stop["stop_id"], 
								time=user_stop["time"],
								num_contributors=1
							)
							break
		
		# Now add the stops that don't fit in any schedules
		# no_schedule_stops
		for stop in no_schedule_stops:
			db_stop = stop["db_stop"]
			user_stop = stop["user_stop"]

			# Find to which schedule this should belong to
			perfect_sch_id = find_perfect_schedule(prominent_routes=prominent_routes, time=user_stop["time"])
			while(1):
				s_id = generate_128bit_id(perfect_sch_id)
				if not get_schedule_info(s_id):
					add_new_schedule(
						s_id=s_id, 
						sch_id=perfect_sch_id, 
						stop_id=db_stop["stop_id"], 
						time=user_stop["time"],
						num_contributors=1
					)
					break


	response = Response(stop, status=200)
	response.headers['Access-Control-Allow-Origin'] = '*';
	return response

@application.route('/test', methods=["GET"])
def rest():
	geocode = Geocode()
	return str(geocode.get_place(lat=11.9838736,lon=75.5545614))

