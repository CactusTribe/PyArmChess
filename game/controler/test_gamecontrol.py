"""Tests of game.controler.GameControl."""

from io import StringIO
import unittest


from game.controler.gamecontrol import GameControl
from game.controler.playercontrol import PlayerControl
from game.model.player import Player
from lib.boardcontrol import InvalidMoveException


class GameControlTest(unittest.TestCase):
    """GameControl test class."""

    player_1 = None
    player_2 = None
    game_control = None
    temp_stdout = None

    def setUp(self):
        """Init tests."""
        self.player_1 = PlayerControl(Player("Foo", human=True))
        self.player_2 = PlayerControl(Player("Bar"))
        self.game_control = GameControl(self.player_1, self.player_2)
        self.temp_stdout = StringIO()

    def test_init(self):
        # GameControl.__init__ sets first player to current_player.
        self.assertIs(self.game_control.current_player, self.player_1)

    def test_end_round(self):
        # GameControl.end_round switchs the current_player.
        self.game_control.end_round()
        self.assertIs(self.game_control.current_player, self.player_2)

    def test_apply_move(self):
        # GameControl.apply_move applies the move to the board.
        old_board = self.game_control.board.copy()
        self.game_control.apply_move("e2e4")
        self.assertNotEqual(old_board.fen(), self.game_control.board.fen())

    def test_apply_move_invalid(self):
        # GameControl.apply_move print the proper error message.
        with self.assertRaises(InvalidMoveException):
            self.game_control.apply_move("e6e8")
