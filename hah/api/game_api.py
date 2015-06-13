from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret
from hah.models.game import Game
from hah import db, errors

class GameApi(restful.Resource):
    method_decorators=[shared_secret]

    def get(self, api_client):
        if api_client.game is None:
            raise errors.NoGameRunningError()

        return api_client.game.serialize()

    def post(self, api_client):
        if api_client.game is not None:
            raise errors.GameAlreadyExistError()

        game = Game()
        api_client.game = game
        db.session.add(game)
        db.session.commit()
        return game.serialize()

    def delete(self, api_client):
        if api_client.game is None:
            raise errors.NoGameRunningError()

        db.session.delete(api_client.game)
        db.session.commit()
        return {}

