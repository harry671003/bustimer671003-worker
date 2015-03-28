from app import application, cm
import logging
from flask import request, Response
import json
from boto.dynamodb2.table import Table

# Home page
@application.route('/', methods=["GET", "POST"])
def index():
	response = None
	if request.json is None:
		# Expect application/json request
		response = Response("NO JSON", status=415)
	else:
		test_table = Table('test', connection=cm.db)
		test_table.put_item(data={
			"id": json.dumps(request.json)
		})
		response = Response("ERROR", status=200)
	return response