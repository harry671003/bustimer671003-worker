from app import application, cm
import logging
from flask import request, Response, jsonify
import json
from boto.dynamodb2.table import Table
import base64
from hashlib import sha1
from datetime import datetime

# Home page
@application.route('/', methods=["PUT", "POST", "GET"])
def index():
	response = None
	decoded = request.get_data()
	test_table = Table('test', connection=cm.db)
	test_table.put_item(data={
		"id": sha1(str(datetime.now())),
		"data": decoded
	})
	response = Response("OK!", status=200)
	return response