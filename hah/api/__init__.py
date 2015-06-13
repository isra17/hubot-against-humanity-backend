from flask.ext import restful
from hah.api import game_api

def Api(app):
    api = restful.Api(app)

    api.add_resource(game_api.GameApi, '/game')

