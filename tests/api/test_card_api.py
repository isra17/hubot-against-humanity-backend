from freezegun import freeze_time
from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.api_client import ApiClient
from hah.models.card import Card
from tests.factory_boy.game_factory import GameFactory
from tests.factory_boy.player_factory import PlayerFactory
import json

class GameApiTest(HahTest):
    def test_manage_cards(self):
        rv = self.auth_post('/cards', data={'type':'black','text':'Test cards'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        card_id = rv_data['id']
        self.assertIsNotNone(card_id)
        self.assertEqual('black', rv_data['type'])
        self.assertEqual('Test cards', rv_data['text'])

        rv = self.auth_get('/cards')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual(1, len(rv_data))
        self.assertEqual(card_id, rv_data[0]['id'])

        rv = self.auth_delete('/cards/{}'.format(card_id))
        self.assert_200(rv)

        rv = self.auth_get('/cards')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual(0, len(rv_data))
