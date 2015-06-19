from freezegun import freeze_time
from tests.hahtest import HahTest
from tests.factory_boy.player_factory import PlayerFactory
from tests.factory_boy.game_factory import GameFactory
from hah import db, errors
from hah.models.game import Game
from hah.models.card import Card
from hah.models.player import Player

class GameTest(HahTest):
    def test_create_game(self):
        game = Game()
        self.assertEqual(60, game.deck_size)
        self.assertNotEqual(0, game.deck_seed)

    def test_pick_cards(self):
        game = GameFactory(deck_seed=0)
        db.session.commit()

        self.assertEqual([13, 34, 30, 37], [c.id for c in game.pick_white_cards(4)])
        self.assertEqual([45], [c.id for c in game.pick_white_cards(1)])
        self.assertEqual([43], [c.id for c in game.pick_white_cards(1)])
        self.assertEqual(44, len(game.pick_white_cards(50)))
        self.assertEqual([], game.pick_white_cards(1))

    def test_game_ready_players_played(self):
        game = GameFactory()
        game.players.append(PlayerFactory(id='U1'))
        game.players.append(PlayerFactory(id='U2'))
        game.players.append(PlayerFactory(id='U3'))
        game.players.append(PlayerFactory(id='U4'))
        game.start_turn()

        game.players[1].played_card = Card.query.get(11)
        with self.assertRaises(errors.NotEnoughPlayers):
            game.check_turn_ready()

        game.players[2].played_card = Card.query.get(12)
        with self.assertRaises(errors.TooEarly):
            game.check_turn_ready()

        game.players[3].played_card = Card.query.get(13)
        self.assertTrue(game.check_turn_ready())

    def test_game_ready_time_delay(self):
        game = GameFactory()
        game.players.append(PlayerFactory(id='U1'))
        game.players.append(PlayerFactory(id='U2'))
        game.players.append(PlayerFactory(id='U3'))
        game.players.append(PlayerFactory(id='U4'))

        with freeze_time("2000-01-01 12:00:00"):
            game.start_turn()
            game.players[1].played_card = Card.query.get(11)
            game.players[2].played_card = Card.query.get(12)
            with self.assertRaises(errors.TooEarly):
                game.check_turn_ready()
        with freeze_time("2000-01-01 12:00:20"):
            self.assertTrue(game.check_turn_ready())

