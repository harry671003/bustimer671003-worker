from app import application
print "views"
# Application routes defined here
@application.route('/index')
def index():
    return "Hello World!"
