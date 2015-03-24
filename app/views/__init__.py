from app import application
import logging
from flask import request, Response

# Home page
@application.route('/', methods=["GET", "POST"])
def index():
	response = None
	if request.json is None:
		# Expect application/json request
		response = Response("NO JSON", status=415)
	else:
		logging.log('Error processing message: %s' % request.json)
		response = Response("ERROR", status=500)
	return response