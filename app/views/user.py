from app import application, cm
from flask import request
from flask.ext.login import LoginManager
import json
from lib.helpers import message as message_helper
import os

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound

base_url = '/user'

@application.route(base_url + '/login', methods=['POST'])
def login():
	return message_helper.success()

# Register a device to BusTimer
# 
@application.route(base_url + '/register_device', methods=['POST'])
def register_device():
	# Check for the device_id in POST request
	device_id = request.form.get("device_id")
	if device_id is None:
		return message_helper.error("Please supply a device ID")
	if len(device_id) != 10:
		return message_helper.error("Device ID is not of sufficient length")
	# Device ID validated. Add it to DB
	# Retrieve the table
	try:
		user_table = Table('users', connection=cm.db)
		try:
			# Check if already there is a device_id
			is_existing_id = user_table.get_item(device_id=device_id)
			return message_helper.error("Sorry: ID Already existing")
		except ItemNotFound, e:
			# The item not found
			# Insert the device_id to table
			user_table.put_item(data={
				"device_id": device_id
			})
	except Exception, e:
		# If the application is in debug mode
		if application.debug:
			return message_helper.error(str(e))
		else:
			return message_helper.error("Sorry, An error occured")
	return message_helper.success()