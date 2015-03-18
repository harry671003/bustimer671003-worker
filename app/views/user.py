from app import application
from flask import request
from flask.ext.login import LoginManager
import json
from lib.helpers import message as message_helper
import os

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(application)


@application.route('/user/login', methods=['POST'])
def login():
	return message_helper.success()

@application.route('/user/signup', methods=['POST'])
def signup():
	return "signup"

@application.route('/user/signup', methods=['GET'])
def signup():
	return str(os.environ)