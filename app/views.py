from app import application
print "views"
# Application routes defined here
@application.route('/f/', endpoint='v1')
@application.route('/index', methods=["GET", "POST"], endpoint='v2')
def index():
    return "Hello World!"
