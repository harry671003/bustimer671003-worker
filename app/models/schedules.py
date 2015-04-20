from lib.helpers.tables import tb_schedule
from boto.dynamodb2.exceptions import ItemNotFound
# Query for schedule given a stop_id and a stop_time
def query_schedule(stop_id, stop_time, threshold):
	threshold = int(threshold)
	return tb_schedule.query_2(
		stop_id__eq=stop_id,
		time__lt=stop_time + threshold,
		time__gt=stop_time - threshold,
		index='stop_id_index'
	)

# Update the time centroid
def update_time_centroid(schedule_info, new_time):
	num_contributors = schedule_info["num_contributors"]
	# old time
	old_time = int(schedule_info["time"])

	numerator = float(old_time * num_contributors + new_time)
	denominator = float(num_contributors + 1)
	updated_time =  int(numerator/denominator)

	# update the db
	schedule_info["time"] = updated_time
	schedule_info["num_contributors"] += 1
	schedule_info.save()

# Get schedule given sch_id and stop_id
def get_schedule(sch_id, stop_id):
	result = tb_schedule.query_2(
		stop_id__eq=stop_id,
		sch_id__eq=sch_id,
		index='sch_id_index'
	)

	result = list(result)
	if len(result) > 0:
		return result[0]
	else:
		return None

# Check schedule id
def check_schedule_existing(sch_id):
	result = tb_schedule.query_2(
		sch_id__eq=sch_id,
		index='sch_id_index'
	)
	result = list(result)
	if len(result) == 0:
		return False
	else:
		return True

# Get schedule duration
def get_schedule_duration(sch_id):
	schedule = tb_schedule.query_2(
		sch_id__eq=sch_id,
		index='sch_id_index'
	)
	start_time = None
	end_time = None


	first = True
	for stop in schedule:
		# For the first item set the 
		# start and end time as that time
		if first:
			first = False
			start_time = stop["time"]
			end_time = stop["time"]

		else:
			if stop["time"] < start_time: # Find if applicable for new start time
				start_time = stop["time"]
			elif stop["time"] > end_time: # Find if applicable for new stop time
				stop_time = stop["time"]
			else:
				pass

	return {
		"start": start_time,
		"stop": end_time
	}

def get_schedule_info(s_id):
	try:
		stop = tb_schedule.get_item(id=s_id)
		return stop
	except ItemNotFound,e:
		None
# Add a new schedule
def add_new_schedule(s_id, sch_id, stop_id, time, num_contributors):
	tb_schedule.put_item(
		data={
			'id': s_id,
			'sch_id': sch_id,
			'stop_id': stop_id,
			'time': time,
			'num_contributors': num_contributors
		}
	)