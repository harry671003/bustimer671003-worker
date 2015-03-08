#!flask/bin/python
from flask                          import Flask, render_template, request, session, flash, redirect, jsonify, json
from ConfigParser                   import ConfigParser
import os, time, sys, argparse

from app import application

application.debug = True

# Get the port to run on
server_port = None
# Check whether the app is running on Beanstalk
# If the app is running on beanstalk the configuration
# file will be loaded and SERVER_PORT will be set as 80
if 'SERVER_PORT' in os.environ:
    server_port = int(os.environ['SERVER_PORT'])

# Check if it is a local computer
if server_port is None:
    server_port = 5000

# Run the application
application.run(debug=True, port=server_port, host='0.0.0.0')