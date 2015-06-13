from flask import request, abort, current_app
from functools import wraps
from hah.models.api_client import ApiClient
from hah import errors

def ensure_game(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'api_client' not in kwargs:
            abort(500)
        game = kwargs['api_client'].game
        if game is not None:
            kwargs['game'] = game
            return func(*args, **kwargs)
        raise errors.NoGameRunningError
    return wrapper


def shared_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_client = ApiClient.query \
            .filter_by(shared_secret=request.headers.get('X-Secret-Token')) \
            .first()
        if api_client is not None:
            kwargs['api_client'] = api_client
            return func(*args, **kwargs)
        abort(401)
    return wrapper

