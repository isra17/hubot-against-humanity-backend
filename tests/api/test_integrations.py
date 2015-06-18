from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.api_client import ApiClient
from hah.models.card import Card
from tests.factory_boy.game_factory import GameFactory
from tests.factory_boy.player_factory import PlayerFactory
import json

class GameApiTest(HahTest):
    def test_game(self):
        rv = self.auth_post('/game')
        self.assert_200(rv)

        rv = self.auth_post('/game/players', data={'id':'U1'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual(10, len(rv_data['cards']))
        self.assertTrue(all('white' in c for c in rv_data['cards']))

        rv = self.auth_get('/game')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual('U1', rv_data['active_player'])
        self.assertIn('black', rv_data['active_card'])


        rv = self.auth_post('/game/players', data={'id':'U2'})
        self.assert_200(rv)

        rv = self.auth_post('/game/players', data={'id':'U3'})
        self.assert_200(rv)

        rv = self.auth_put('/game/players/U2', data={'played_card':'3'})
        self.assert_200(rv)

        rv = self.auth_put('/game/players/U3', data={'played_card':'0'})
        self.assert_200(rv)

        rv = self.auth_post('/game/vote')
        self.assert_200(rv)

        rv = self.auth_post('/game/vote', data={'card': '1'})
        self.assert_200(rv)

