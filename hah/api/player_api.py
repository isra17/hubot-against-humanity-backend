from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.player import Player
from hah import db, errors

class PlayerApi(restful.Resource):
    method_decorators=[ensure_game, shared_secret]

    def post(self, api_client, game):
        player_id = request.form.get('id')
        player = Player(
                id=player_id,
                game_id=game.id)

        db.session.add(player)
        db.session.commit()
        return player.serialize()

