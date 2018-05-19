"""Game controler."""

import platform
import chess
from chess import uci


class InvalidMoveException(Exception):
    """Exception for invalid moves."""

    pass


class GameControl(object):
    """Game controler."""

    board = None
    nb_moves = None

    def __init__(self, player_white, player_black):
        """Game initialisation."""
        self.player_white = player_white
        self.player_black = player_black
        self.current_player = player_white
        self._init_model()
        self._init_engine()

    def _init_model(self):
        self.board = chess.Board()
        self.nb_moves = 0

    def _init_engine(self):
        if platform.system() == "Linux":
            if platform.machine() == "armv7l":
                self.engine = uci.popen_engine("bin/stockfish-8-arm-rasp")
            else:
                self.engine = uci.popen_engine("bin/stockfish-9-popcnt")
        elif platform.system() == "Darwin":
            self.engine = uci.popen_engine("bin/stockfish")
        self.engine.uci()
        self.engine.ucinewgame()

    def new_game(self):
        self.board = chess.Board()
        self.nb_moves = 0

    def compute_best_move(self, movetime):
        """The engine compute the best move from the current position."""
        return self.engine.go(movetime=movetime)

    def apply_move(self, uci_move):
        """Apply the move to the board."""
        try:
            move = chess.Move.from_uci(str(uci_move))
            if move in self.board.legal_moves:
                self.board.push(move)
                self.engine.position(self.board)
                self.end_round()
                self.nb_moves += 1
            else:
                raise InvalidMoveException
        except (Exception, InvalidMoveException):
            raise InvalidMoveException(
                " -> Invalid move. ({})".format(uci_move))

    def end_round(self):
        """Switch the current_player for the next round."""
        self.current_player = (self.player_white if self.current_player
                               == self.player_black else self.player_black)
