from flask.ext import restful
from hah.api import game_api, player_api, card_api

def Api(app):
    api = restful.Api(app)

    api.add_resource(card_api.CardsApi, '/cards')
    api.add_resource(card_api.CardApi, '/cards/<int:card_id>')
    api.add_resource(game_api.GameApi, '/game')
    api.add_resource(game_api.VoteApi, '/game/vote')
    api.add_resource(player_api.PlayersApi, '/game/players')
    api.add_resource(player_api.PlayerApi, '/game/players/<string:player_id>')

