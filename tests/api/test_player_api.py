from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.player import Player
from hah import db
from tests.factory_boy.game_factory import GameFactory
import json

class PlayerApiTest(HahTest):
    def test_join_game(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_post('/game/players', data={'id': 'UA123'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual('UA123', rv_data['id'])

        db.session.refresh(game)
        self.assertEqual('UA123', game.players[0].id)

    def test_join_game_twice(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_post('/game/players', data={'id': 'UA123'})
        self.assert_200(rv)
        rv = self.auth_post('/game/players', data={'id': 'UA123'})
        self.assert_status(rv, 422)

        db.session.refresh(game)
        self.assertEqual(1, len(game.players))
