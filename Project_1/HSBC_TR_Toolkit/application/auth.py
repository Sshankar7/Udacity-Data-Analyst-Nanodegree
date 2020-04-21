from flask import request, make_response, render_template
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        hashedPass = "pbkdf2:sha256:150000$WXy5Hnk9$022e9529863fe2fca59861c94a1db7cafb7cdcfc6d31d1f880da733335aa2b84"
        if auth and auth.username == "WMR" and check_password_hash(hashedPass,auth.password):
            return f(*args, **kwargs)
        return make_response(render_template("login.html"), 401, {'WWW-Authenticate':'Basic Realm = "Login Required"'})
    
    return decorated
