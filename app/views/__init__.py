from app import application, cm, login_manager
from flask.ext.login import current_user
from flask import g, redirect, url_for
from lib.helpers.login import login_required
from app.models.user import User

# Load the user
@login_manager.user_loader
def load_user(userid):
	# Check if user is root
	if userid == "root":
		return User(userid, 1)
	else:
		return None

# Unauthorized access
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the login url
    return redirect(url_for('admin_login'))

# Add current user to Flask Global g
@application.before_request
def before_request():
	g.user = current_user

# Home page
@application.route('/')
@application.route('/index')
def index():
	return "Welcome to Bus App!"

# Add other views
# Add /user/* views
from app.views import user

# Add /config/* views
from app.views import config

# Add /admin/* views
from app.views import admin