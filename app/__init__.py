from flask import Flask
from ConfigParser import ConfigParser
from lib.dynamodb.connection_manager import ConnectionManager
import os


# Create the application
application = Flask(__name__)
application.debug = True
application.secret_key = "dfadfasfafa"


# Read environment variable for whether to read config from EC2 instance metadata
use_instance_metadata = ""
if 'USE_EC2_INSTANCE_METADATA' in os.environ:
    use_instance_metadata = os.environ['USE_EC2_INSTANCE_METADATA']

server_port = None
mode = None
config = None
# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
	server_port = int(os.environ['SERVER_PORT'])
	mode = 'service'
	# Configure the application from the config file
	config = ConfigParser()
	config.read("config")
else:
    server_port = 5000
    mode = 'local'

# Connect to database with the given configurations
cm = ConnectionManager(mode=mode, config=config, endpoint=None, port=None, use_instance_metadata=use_instance_metadata)


# Import the views
from app import views