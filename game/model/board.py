import chess


class Board(object):
    """Board definition."""

    def __init__(self):
        """Initialise the board."""
        self.board = chess.Board()
