#!flask/bin/python
from flask import Flask
import os

from app import application

# Run the application with test server if in local machine
if __name__ == "__main__":
	application.run(debug = True, port=8000, host='0.0.0.0')
