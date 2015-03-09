from app import application

@application.route('/')
def index():
	return "Welcome to Bus App!"

@appliction.route('/user/login')
def login():
	return "login"

@application.route('/user/signup')
def signup():
	return "signup"