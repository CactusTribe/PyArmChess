# pylint: disable = protected-access
"""Tests of game.controler.GameControl."""

from io import StringIO
import unittest

import chess

from game.controler.gamecontrol import GameControl, InvalidMoveException
from game.controler.playercontrol import PlayerControl
from game.model.player import Player


class GameControlTest(unittest.TestCase):
    """GameControl test class."""

    player_1 = None
    player_2 = None
    game_control = None
    temp_stdout = None

    def setUp(self):
        """Init tests."""
        self.player_1 = PlayerControl(Player("Foo", chess.WHITE, human=True))
        self.player_2 = PlayerControl(Player("Bar", chess.BLACK))
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

    def test_init_engine(self):
        # GameControl._init_engine sets stockfish engine.
        self.game_control._init_engine()
        self.assertEqual(self.game_control.engine.name,
                         "Stockfish 9 64 POPCNT")

    def test_compute_best_move(self):
        # GameControl.compute_best_move returns a best move.
        best_move = self.game_control.compute_best_move(10)
        self.assertNotEqual(best_move, None)
