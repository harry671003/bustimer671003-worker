from app import application

@application.route('/')
def index():
	return "Welcome to Bus App!"

# Add /user/* views
from user import views