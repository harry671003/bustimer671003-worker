import urllib2
import urllib
import json
import pprint

from app import cm
from math import radians

from boto.dynamodb2.exceptions import ItemNotFound

# helpers
from lib.helpers.coords import Coords
from lib.helpers.tables import tb_stops, tb_stops_loc
from lib.helpers.security import generate_stopid

class Geocode:
	__earth_radius = 6371

	def __init__(self):
		self.email = "bussingtime@gmail.com"

	# Get the necessary difference between lat and lon
	# for a distance diff of d meters
	def __diff(self,lat, lon, d=300):
		# In kerala the approx diff in lat and lon
		# between two coordinates that are 300 m apart 
		# is 0.004
		return 0.004

	# Search the DB for a place with lat and lon close
	def __search_db(self, lat, lon):
		c = Coords()
		lat = float(lat)
		lon = float(lon)
		lat_part = str(int(lat))

		lat = c.integerify(lat)
		lon = c.integerify(lon)

		diff = c.integerify(self.__diff(lat, lon, 300))

		# Get the count of matching results
		result = tb_stops_loc.query_2(
			lat_part__eq=lat_part,
			lat__gt=lat - diff,
			lat__lt=lat + diff,
			index='lat_index'
		)

		result = list(result)
		if len(result) == 0:
			return None

		# Now loop through longitudes
		for item in result:
			if item["lon"] <= lon + diff and item["lon"] >= lon - diff:
				# Get the other data
				return item["stop_id"]

		return None

	# Geocode from google maps api
	def __search_gmap(self, lat, lon):
		url = "https://maps.googleapis.com/maps/api/geocode/json"

		# params
		params = {
			"key": "AIzaSyBgnjJupi9HeTxrHKbNLMuB06BMfrHgWNM",
			"latlng": str(lat) + "," + str(lon),
		}

		# First check for a busstop
		params["result_type"] = "bus_station"
		# Encode the parameters in url
		data = urllib.urlencode(params)

		# Send request to nominatim servers
		request = urllib2.Request(url + "?" + data)

		response = urllib2.urlopen(request)


		# Get the geo coded data
		geocoded = json.loads(response.read())
		# Extract the place details
		place_data = {
			"name": None,
			"lat": None,
			"lon": None,
			"country": None,
			"level_1": None,
			"level_2": None
		}

		# Check the status
		status = geocoded["status"]
		if status == "OK":
			# Successfully got the bus station

			# Get the top result
			top_result = geocoded["results"][0]

			# Go through each address components and get the necessary 
			# details
			for addr_comp in top_result["address_components"]:
				addr_types = addr_comp["types"]
				# Check for busstation
				if place_data["name"] is None:
					if "bus_station" in addr_types or \
						"transit_station" in addr_types:
						place_data["name"] = addr_comp["long_name"]
						continue
				
				# Check for level_2
				if place_data["level_2"] is None:
					if "administrative_area_level_2" in addr_types:
						place_data["level_2"] = addr_comp["long_name"]
						continue

				# Check for level_1
				if place_data["level_1"] is None:
					if "administrative_area_level_1" in addr_types:
						place_data["level_1"] = addr_comp["long_name"]
						continue

				# Check for country
				if place_data["country"] is None:
					if "country" in addr_types:
						place_data["country"] = addr_comp["long_name"]
						continue

			try:
				# Get the original lat and lon
				lat = top_result["geometry"]["location"]["lat"]
				lon = top_result["geometry"]["location"]["lon"]
			except KeyError:
				# If not present set to
				# original
				place_data["lat"] = lat
				place_data["lon"] = lon
		elif status == "ZERO_RESULTS":
			# No results found
			return None
		elif status == "OVER_QUERY_LIMIT":
			# Query limit passed
			return None
		else:
			# Other errors
			# server, request denied, invalid request
			return None
		return place_data

	# Reverse geo-coding
	# Convert a lat and long to place name
	def get_place(self, lat, lon):

		# First search the db
		db_result = self.__search_db(lat, lon)

		if db_result:
			return db_result

		# The result is not found in the db
		# Search google maps for that
		gmap_result = self.__search_gmap(lat,lon)

		if(gmap_result is not None):
			# Add this place to database
			# Create a stop_id
			while 1:
				stop_data = {
					"stop_id": generate_stopid(gmap_result["name"])
				}
				# Check if the id already exists
				try:
					print "[+] start get"
					tb_stops.get_item(stop_id=stop_data["stop_id"])
					print "[+] end get"
				except ItemNotFound, e:
					print "[+] excetpion"
					break

			# Append the other data
			stop_data["name"] 		= gmap_result["name"].lower()
			stop_data["name_part"] 	= gmap_result["name"][:1].lower()
			stop_data["level_1"] 	= gmap_result["level_1"].lower()
			stop_data["level_2"] 	= gmap_result["level_2"].lower()
			stop_data["country"] 	= gmap_result["country"].lower()

			# insert to table
			tb_stops.put_item(data=stop_data)

			c = Coords()
			# Append stop_loc data
			stop_loc_data = {
				"stop_id": stop_data["stop_id"],
				"lat_part": str(int(gmap_result["lat"])),
				"lat": c.integerify(gmap_result["lat"]),
				"lon": c.integerify(gmap_result["lon"])
			}

			# insert into stop_loc table
			tb_stops_loc.put_item(data=stop_loc_data)

			# return the stop_id
			return stop_data["stop_id"]

		# Cannot resolve the lat,lon using neither
		return None




		
