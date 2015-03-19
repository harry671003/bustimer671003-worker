from app import application
from app.models.user import User
from flask import request, render_template, g, url_for, redirect
from flask.ext.login import login_user, logout_user, current_user
import json
from lib.helpers import message as message_helper
import os

from app.forms.login import LoginForm

base_url = '/admin'

# Route for admin index page
@application.route(base_url  + '/index')
def admin_index():
	return "ADmin Index"

# Route for admin login page
@application.route(base_url + '/login', methods=['POST', 'GET'])
def admin_login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm(request.form)
	if request.method == "POST" and form.validate():
		if request.form['username'] == "root" and request.form['password'] == os.environ['ROOT_PASS']:
			user = User("root", 1)
			login_user(user)
			return redirect(url_for('admin_index'))
		else:
			return render_template('admin_login.html', error="Invalid username or password", form=form)
	return render_template('admin_login.html', form=form)

# Route for admin logout page
@application.route(base_url  + '/logout')
def logout():
	logout_user()
	return redirect(url_for('admin_login'))