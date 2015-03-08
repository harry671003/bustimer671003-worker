from app import application
print "views"
# Application routes defined here
@application.route('/f/')
@application.route('/index', methods=["GET", "POST"])
def index():
    return "Hello World!"
