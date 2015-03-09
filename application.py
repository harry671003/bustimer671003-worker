from flask                          import Flask, render_template, request, session, flash, redirect, jsonify, json
import os, time, sys, argparse

application = Flask(__name__)
application.debug = True

# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
    serverPort = int(os.environ['SERVER_PORT'])

if serverPort is None:
    serverPort = 5000

@application.route('/')
def index():
	return "Hello World"

if __name__ == "__main__":
        application.run(debug = True, port=serverPort, host='0.0.0.0')
