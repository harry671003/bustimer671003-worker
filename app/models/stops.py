from lib.helpers.tables import tb_stops

def get_stop(stop_id):
	try:
		stop = tb_stops.get_item(stop_id=stop_id)	
		return stop
	except:
		return None
	
