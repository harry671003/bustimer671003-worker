from app import application

@application.route('/user/login')
def login():
	return "login"

@application.route('/user/signup')
def signup():
	return "signup"