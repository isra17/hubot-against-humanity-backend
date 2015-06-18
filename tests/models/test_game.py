from tests.hahtest import HahTest
from tests.factory_boy.player_factory import PlayerFactory
from tests.factory_boy.game_factory import GameFactory
from hah import db
from hah.models.game import Game
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

