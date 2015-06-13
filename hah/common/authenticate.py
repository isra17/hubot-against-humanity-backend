from flask import request, abort, current_app
from functools import wraps
from hah.models.api_client import ApiClient

def shared_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_client = ApiClient.query \
            .filter_by(shared_secret=request.headers.get('X-Secret-Token')) \
            .first()
        if api_client is not None:
            func.__self__.api_client = api_client
            return func(*args, **kwargs)
        abort(401)
    return wrapper

