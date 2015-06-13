from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret, game_running
from hah.models.game import Game
from hah import db, errors

class PlayerApi(restful.Resource):
    method_decorators=[shared_secret, game_running]

    def get(self):
        return {
            'id': 1,
            'player': [],
            'turn': 0
        }

    def post(self):
        if self.api_client.game is not None:
            raise GameAlreadyExistError()

        game = Game(**GameApi.params())
        db.session.add(game)
        db.session.commit()
        return game.serialize()

    def params():
        return {
            'name': request.form.get('name')
        }


