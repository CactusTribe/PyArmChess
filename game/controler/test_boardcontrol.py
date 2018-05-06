import unittest

from game.controler.boardcontrol import BoardControl
from game.model.board import Board


class BoardControlTest(unittest.TestCase):
    """BoardControl test class."""

    def setUp(self):
        """Init tests."""
        self.board = Board()
        self.boardcontrol = BoardControl(self.board)

    def test_next_move(self):
        # BoardControl.apply_next_move returns None.
        result = self.boardcontrol.apply_next_move()
        self.assertIsNone(result)
