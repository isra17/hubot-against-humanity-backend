from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.api_client import ApiClient
from hah import db
from tests.factory_boy.game_factory import GameFactory
import json

class PlayerApiTest(HahTest):
    def test_join_game(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_post('/game/players', data={'id': 123})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual(123, rv_data['id'])

        db.session.refresh(game)
        self.assertEqual(123, game.players[0].id)

