import unittest

import chess

from game.controler.playercontrol import PlayerControl
from game.model.player import Player


class PlayerControlTest(unittest.TestCase):
    """PlayerControl test class."""

    def setUp(self):
        """Init tests."""
        self.player = Player("Joueur1", chess.WHITE, human=True)
        self.playercontrol = PlayerControl(self.player)

    def test_win_game(self):
        self.playercontrol.win_game()
        self.assertGreater(self.player.score, 0)
