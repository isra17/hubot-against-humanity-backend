from functools import wraps
from flask import request, abort
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.player import Player
from hah import db, errors

class PlayersApi(restful.Resource):
    method_decorators=[ensure_game, shared_secret]

    def post(self, api_client, game):
        json = request.get_json()
        player_id = json['id'] if json else None
        if player_id is None:
            raise errors.ParametersMissing('player_id')
        if game.players.filter_by(id=player_id).first() is not None:
            raise errors.PlayerAlreadyJoinedError()

        player = Player(
                id=player_id,
                game=game)

        player.pick_cards()

        if game.active_player is None:
            game.set_active_player(player)

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

    def put(self, api_client, game, player):
        json = request.get_json()
        card = int(json['played_card']) if json else None
        if card is None:
            raise errors.ParametersMissing('played_card')
        if card >= len(player.cards):
            raise errors.InvalidCard()
        if game.active_player.id == player.id:
            raise errors.PlayerCantPlayer

        player.played_card = player.cards[card]
        db.session.commit()
        return player.serialize()

    def delete(self, api_client, game, player):
        db.session.delete(player)
        db.session.commit()
        return {}

class VoteApi(restful.Resource):
    method_decorators=[ensure_player, ensure_game, shared_secret]

    def post(self, api_client, game, player):
        return {}
