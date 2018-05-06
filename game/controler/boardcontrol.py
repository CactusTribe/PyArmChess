"""Board controler"""

import chess
from game.model.board import Board


class BoardControl(object):
    """Interact with model."""

    def __init__(self, chess_board):
        """Board control initialisation."""
        self.board = chess_board.board
        self.next_move = None

    def apply_next_move(self):
        """Apply the next move to the board."""
        self.next_move = "e2e4"
        move = chess.Move.from_uci(self.next_move)
        if move in self.board.legal_moves:
            self.board.push(move)
