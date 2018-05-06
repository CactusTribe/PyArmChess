import unittest

from game.game import Game


class GameTest(unittest.TestCase):
    """GameTest class."""

    def setUp(self):
        """Init tests."""
        self.game = Game()

    def test_init_game(self):
        self.game.new_game()
        print(self.game.board)
