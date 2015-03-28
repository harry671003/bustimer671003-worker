from app import application, cm
import logging
from flask import request, Response, jsonify
import json
from boto.dynamodb2.table import Table

# Home page
@application.route('/', methods=["PUT", "POST", "GET"])
def index():
	response = None
	data = request.data
	test_table = Table('test', connection=cm.db)
	test_table.put_item(data={
		"id": data
	})
	response = Response("OK!", status=200)
	return response