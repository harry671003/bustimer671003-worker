from flask.ext.login import current_user, current_app
from functools import wraps

# login_required function
# This is an improvement over flask-login's login_required
# This implementation supports clearance levels
# A route can be accessed by anyone having a clearance level less than the 
# set clearance level
def login_required(clearance="100"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
               return current_app.login_manager.unauthorized()
            current_app.login_manager.reload_user()
            u_clearance = current_user.get_clearance()
            if (u_clearance > clearance):
                return current_app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper