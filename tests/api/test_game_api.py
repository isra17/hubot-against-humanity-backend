from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.api_client import ApiClient
from hah.models.card import Card
from tests.factory_boy.game_factory import GameFactory
from tests.factory_boy.player_factory import PlayerFactory
import json

class GameApiTest(HahTest):
    def test_create_game(self):
        rv = self.auth_post('/game', data={'channel':'#slackagainsthumanity'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertIn('id', rv_data)
        self.assertEqual(0, rv_data['turn'])

        game = Game.query.get(rv_data['id'])
        self.assertIsNotNone(game)
        self.assertIsNotNone(ApiClient.query.first().game)
        self.assertEqual(60, game.deck_size)

    def test_create_game_already_exist(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_post('/game')
        self.assertStatus(rv, 422)

    def test_get_game(self):
        game = GameFactory()
        game.active_player = PlayerFactory(id='U1')
        game.active_player.played_card = Card.query.first()
        self.api_client.game = game

        rv = self.auth_get('/game')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertIn('id', rv_data)
        self.assertEqual(0, rv_data['turn'])
        self.assertEqual('U1', rv_data['active_player'])
        self.assertEqual('black card 0', rv_data['active_card'])

    def test_delete_game(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_delete('/game')
        self.assert_200(rv)

        self.assertIsNone(ApiClient.query.first().game)

