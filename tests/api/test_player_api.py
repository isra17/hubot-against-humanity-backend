from tests.hahtest import HahTest
from hah.models.game import Game
from hah.models.player import Player
from hah import db
from tests.factory_boy.game_factory import GameFactory
from tests.factory_boy.player_factory import PlayerFactory
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
        self.assertEqual(1, game.players.count())

    def test_leave_game(self):
        game = GameFactory()
        self.api_client.game = game
        game.players.append(PlayerFactory(id='UA1'))

        rv = self.auth_delete('/game/players/UA1')
        self.assert_200(rv)

        self.assertEqual(0, game.players.count())

    def test_pick_cards_on_create(self):
        game = GameFactory(deck_seed=0)
        self.api_client.game = game
        db.session.commit()

        rv = self.auth_post('/game/players', data={'id': 'UA1'})
        self.assert_200(rv)

        db.session.refresh(game)
        self.assertEqual([13, 30, 34, 37, 43, 45, 48, 51, 56, 59], [c.id for c in Player.query.get('UA1').cards])
        self.assertTrue(game.white_cards_picked >= 10)

    def test_get_player(self):
        game = GameFactory(deck_seed=0)
        self.api_client.game = game
        game.players.append(PlayerFactory(id='UA1'))

        rv = self.auth_get('/game/players/UA1')
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual('UA1', rv_data['id'])

    def test_no_player_id(self):
        game = GameFactory(deck_seed=0)
        self.api_client.game = game

        rv = self.auth_post('/game/players')
        self.assert_status(rv, 422)

    def test_first_player_join(self):
        game = GameFactory(deck_seed=0)
        self.api_client.game = game

        rv = self.auth_post('/game/players', data={'id':'U1'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertEqual('U1', game.active_player.id)
        self.assertEqual(6, game.active_player.played_card.id)

