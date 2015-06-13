from flask.ext import restful
from hah.api import game

def Api(app):
    api = restful.Api(app)

    api.add_resource(game.Game, '/game')

