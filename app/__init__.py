from flask import Flask


# Create the application
application = Flask(__name__)
application.debug = True
application.secret_key = "dfadfasfafa"

# Import the views
from app import views