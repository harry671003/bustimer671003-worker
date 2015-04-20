# xhd time is a way to store time
# as a decimal
# It is taken as the number of seconds from 12:00 am
# it is a value between 0 and 86400
def get_xhd_from_time(hour=0, minute=0, second=0):
	# boundary check
	if(hour < 24 and hour >= 0 and 
		minute < 60 and minute >= 0 and
		second < 60 and second >= 0):
		return hour * 3600 + minute * 60 + second
	else:
		return None

# convert xhd to normal time
def get_time_from_xhd(xhd):
	try:
		xhd = int(xhd)
	except:
		return None
	# Boundary check
	if(not (xhd >= 0 and xhd < 3600 * 24)):
		return None
	# Calculate hours
	hour = xhd // 3600
	
	# Calculate minutes
	xhd = xhd % 3600
	minute = xhd // 60
	
	# Calculate seconds
	xhd = xhd % 60
	second = xhd

	return {
		"hour"		: hour,
		"minute" 	: minute,
		"second"	: second
	}

def get_time_str(hour=0, minute=0, second=0):
	return "%02d:%02d" % (hour, minute)