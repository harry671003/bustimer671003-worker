#!flask/bin/python
from flask import Flask
import os

application = Flask(__name__)
application.debug = True

server_port = None
# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
    server_port = int(os.environ['SERVER_PORT'])

if server_port is None:
    serverPort = 5000

@application.route('/')
def index():
	return "Hello World"

if __name__ == "__main__":
        application.run(debug = True, port=server_port, host='0.0.0.0')
