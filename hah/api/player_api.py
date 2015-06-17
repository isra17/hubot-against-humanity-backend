from functools import wraps
from flask import request, abort
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.player import Player
from hah import db, errors

class PlayersApi(restful.Resource):
    method_decorators=[ensure_game, shared_secret]

    def post(self, api_client, game):
        player_id = request.form.get('id')
        if game.players.filter_by(id=player_id).first() is not None:
            raise errors.PlayerAlreadyJoinedError()

        player = Player(
                id=player_id,
                game=game)

        player.pick_cards()

        db.session.add(player)
        db.session.commit()
        return player.serialize()

def ensure_player(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'game' not in kwargs:
            abort(422)
        game = kwargs['game']
        player_id = kwargs.pop('player_id')
        player = game.players.filter_by(id=player_id).first()
        if player is not None:
            kwargs['player'] = player
            return func(*args, **kwargs)
        abort(404)
    return wrapper

class PlayerApi(restful.Resource):
    method_decorators=[ensure_player, ensure_game, shared_secret]

    def get(self, api_client, game, player):
        return player.serialize()

    def delete(self, api_client, game, player):
        db.session.delete(player)
        db.session.commit()
        return {}
