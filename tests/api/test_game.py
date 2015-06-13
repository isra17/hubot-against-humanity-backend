from tests.hahtest import HahTest
from hah.models.game import Game
import json

class GameTest(HahTest):
    def test_create_game(self):
        Game.query.delete()

        rv = self.auth_post('/game')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        game = Game.query.get(rv_data['id'])
        self.assertIsNotNone(game)
