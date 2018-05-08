"""Board controler"""

import chess
from lib.boardcontrol import InvalidMoveException


class BoardControl(object):
    """Interact with model."""

    def __init__(self, board):
        """Board control initialisation."""
        self.board = board
        self.next_move = None

    def apply_move(self, uci_move):
        """Apply the next move to the board."""
        move = chess.Move.from_uci(uci_move)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            raise InvalidMoveException
