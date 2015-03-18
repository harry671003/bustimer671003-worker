from app import application, config, cm

# Home page
@application.route('/')
@application.route('/index')
def index():
	return "Welcome to Bus App!"


# Add /user/* views
from app.views import user

# Add /config/* views
from app.views import config
