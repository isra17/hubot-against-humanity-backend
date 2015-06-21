from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.api_client import ApiClient
from hah.models.card import Card
from tests.factory_boy.game_factory import GameFactory
from tests.factory_boy.player_factory import PlayerFactory
from unittest.mock import patch
import json

class GameApiTest(HahTest):
    @patch('os.urandom')
    def test_game(self, urandom):
        urandom.return_value = b'\x00'*4
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
        active_card = rv_data['active_card']

        rv = self.auth_post('/game/players', data={'id':'U2'})
        self.assert_200(rv)

        rv = self.auth_post('/game/players', data={'id':'U3'})
        self.assert_200(rv)

        rv = self.auth_put('/game/players/U2', data={'played_card':'3'})
        self.assert_200(rv)

        rv = self.auth_put('/game/players/U3', data={'played_card':'0'})
        self.assert_200(rv)

        rv = self.auth_get('/game/vote')
        self.assert_200(rv)

        rv = self.auth_post('/game/vote', data={'player': 'U1', 'card': '1'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual('U3', rv_data['voted_player'])
        self.assertEqual(1, rv_data['turn'])
        self.assertEqual('U2', rv_data['active_player'])
        self.assertEqual(1, rv_data['players'][2]['score'])
        self.assertNotEqual(active_card, rv_data['active_card'])
        self.assertTrue(all(len(p['cards']) == 10 for p in rv_data['players']))

