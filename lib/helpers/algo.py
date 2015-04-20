def find_perfect_schedule(prominent_routes, time):
	time = int(time)
	# Assuming that prominent_routes is sorted
	for route in prominent_routes:
		if time < route["stop"]:
			return route["sch_id"]

	# finally if we reach here that means 
	# all the routes has been considered
	# so just return the last route
	return prominent_routes[len(prominent_routes)-1]["sch_id"]