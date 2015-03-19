from app import application, cm
from flask import request, Response, render_template
from flask.ext.login import LoginManager
from lib.helpers.login import login_required
import json
from lib.helpers import message as message_helper
# Get the connection manager
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table

# Base Url for this app 
base_url = '/config'

# setup the db
@application.route(base_url + '/setupdb', methods=['GET'])
@login_required(1)
def setup_db():
	# Create the users table
	try:
		# Check if Users table exist
		cm.db.describe_table('users')
	except Exception, e:
		# Users table doesn't exist. So create it
		users = Table.create('users', schema=[
				HashKey('device_id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, connection=cm.db
		)

	# Create the bus table
	try:
		# Check if Bus table exist
		cm.db.describe_table('bus')
	except Exception, e:
		# bus table doesn't exist. So create it
		users = Table.create('bus', schema=[
				HashKey('bus_id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, connection=cm.db
		)
	
	# Create the bus-stops table
	try:
		cm.db.describe_table('bus_n_stops')
	except Exception, e:
		users = Table.create('bus_n_stops', schema=[
				HashKey('id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, 
			global_indexes= [
				GlobalAllIndex('bus_id_index', parts=[
					HashKey('bus_id'),
				]),
				GlobalAllIndex('stop_id_index', parts=[
					HashKey('stop_id'),
				]),
			],
			connection=cm.db
		)

	# Create the stops table
	try:
		cm.db.describe_table('stops')
	except Exception, e:
		users = Table.create('stops', schema=[
				HashKey('stop_id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, 
			global_indexes= [
				GlobalAllIndex('lat_lon_index', parts=[
					HashKey('lat'),
					RangeKey('lon')
				]),
				GlobalAllIndex('stop_name_index', parts=[
					HashKey('name'),
				]),
			],
			connection=cm.db
		)

	return "Done!"

@application.route(base_url + '/showdb', methods=['GET'])
@login_required(1)
def show_db():
	tables = cm.db.list_tables()
	table_data = []
	for table in tables["TableNames"]:
		# out += type(table)
		table_data.append(cm.db.describe_table(table))
	return render_template('describe_tables.html', table_data=table_data)
