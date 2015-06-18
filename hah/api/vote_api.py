from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.game import Game
from hah import db, errors

class VoteApi(restful.Resource):
    method_decorators=[ensure_game, shared_secret]

    def post(self, api_client, game):
        return {}

