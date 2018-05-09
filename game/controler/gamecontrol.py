"""Game controler."""

import chess

from game.controler.boardcontrol import BoardControl
from lib.boardcontrol import InvalidMoveException


class GameControl(object):
    """Game controler."""

    def __init__(self, player_white, player_black):
        """Game initialisation."""
        self.player_white = player_white
        self.player_black = player_black
        self.current_player = player_white
        self.board = chess.Board()
        self.boardcontrol = BoardControl(self.board)

    def apply_move(self, uci_move):
        """Apply the move to the board."""
        try:
            self.boardcontrol.apply_move(uci_move)
            self.end_round()
        except InvalidMoveException:
            raise InvalidMoveException

    def end_round(self):
        """Switch the current_player for the next round."""
        self.current_player = (self.player_white if self.current_player
                               == self.player_black else self.player_black)
