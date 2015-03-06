#!flask/bin/python
from flask                          import Flask, render_template, request, session, flash, redirect, jsonify, json
from ConfigParser                   import ConfigParser
import os, time, sys, argparse

application = Flask(__name__)
application.debug = True

@application.route('/')
@application.route('/index', methods=["GET", "POST"])
def index():
    return "Hello World!"

if __name__ == "__main__":
    application.run(debug = True, host='0.0.0.0')
