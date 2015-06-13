from flask import request, abort, current_app
from functools import wraps

def shared_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.config['SHARED_SECRET'] == request.headers.get('X-Secret-Token'):
            return func(*args, **kwargs)
        abort(401)
    return wrapper

