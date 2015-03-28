from app import application, cm
import logging
from flask import request, Response
import json

# Home page
@application.route('/', methods=["GET", "POST"])
def index():
	response = None
	test_table = Table('test', connection=cm.db)
	test_table.put_item(data={
		"id": json.dumps(request)
	})
	response = Response("ERROR", status=200)
	return response