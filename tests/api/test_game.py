from tests.hahtest import HahTest

class GameTest(HahTest):
    def test_create_game(self):
        rv = self.auth_post('/game')
        self.assert_200(rv)
