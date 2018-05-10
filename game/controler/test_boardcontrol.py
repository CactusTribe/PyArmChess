"""Tests of game.controler.BoardControl."""

import unittest
import chess

from game.controler.boardcontrol import BoardControl
from lib.boardcontrol import InvalidMoveException


class BoardControlTest(unittest.TestCase):
    """BoardControl test class."""

    def setUp(self):
        """Init tests."""
        self.board = chess.Board()
        self.boardcontrol = BoardControl(self.board)

    def test_apply_move(self):
        # BoardControl.apply_move doesn't raises InvalidMoveException.
        self.boardcontrol.apply_move("e2e4")

    def test_apply_move_invalid(self):
        # BoardControl.apply_move raises InvalidMoveException.
        with self.assertRaises(InvalidMoveException):
            self.boardcontrol.apply_move("e6e8")
