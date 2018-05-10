"""Main class of the program.

Run this script to run the game and interact with a prompt.
"""
import time
from collections import OrderedDict

import chess

from game.controler.gamecontrol import GameControl
from game.controler.playercontrol import PlayerControl
from game.model.player import Player


class InvalidCommandException(Exception):
    """Invalid command exception."""

    pass


class PyArmChess(object):
    """PyArmChess definition."""

    def __init__(self, interactive=False):
        """Initialisation."""
        self.running = False
        self.interactive = interactive
        self.commands = {"q": self.quit,
                         "quit": self.quit,
                         "print": self.print_board,
                         "move": self.set_move,
                         "demo": self.play_demo,
                         "new": self._init_game}
        self.logs = OrderedDict()
        self.log_text("-"*80)
        self._init_chess_camera()
        self._init_game()

    def _init_game(self):
        self.log_text(" -> Create new chessboard ...")
        self.player_1 = PlayerControl(Player("Foo", chess.WHITE, human=True))
        self.player_2 = PlayerControl(Player("Bar", chess.BLACK))
        self.game_control = GameControl(self.player_1, self.player_2)
        if self.interactive:
            self.print_player_color()

    def _init_chess_camera(self):
        self.log_text(" -> Init ChessCamera ...")

    def run(self):
        self.running = True
        while self.running:
            try:
                input_cmd = input("$ ")
                input_raw = str(input_cmd).strip().split()
                args_cmd = input_raw[1::]
                self.execute_command(input_raw[0], *args_cmd)
            except Exception as exc:
                self.log_text(str(exc))

    def execute_command(self, command, *args):
        if command in self.commands.keys():
            self.commands[command](*args)
        else:
            raise InvalidCommandException(" -> Invalid command.")

    def log_text(self, text, print_log=True):
        timestamp = int(time.time())
        self.logs[timestamp] = text
        if self.interactive and print_log:
            print(text)

    def get_last_log(self):
        timestamp = list(self.logs.keys())[-1]
        return self.logs[timestamp]

    def print_board(self):
        self.log_text(str(self.game_control.board), print_log=False)
        if self.interactive:
            str_board = str(self.game_control.board)
            list_board = [str_board[i:i+16]
                          .strip("\n")
                          .replace(" ", "")
                          for i in range(0, len(str_board), 16)]
            print("")
            for index, line in enumerate(list_board):
                print(8 - index, "|", ' '.join(line))
            print("  ", ''.join("-" * 16))
            print("   ", ' '.join("ABCDEFGH"))
            print("")

    def set_move(self, uci_move):
        self.game_control.apply_move(uci_move)
        self.print_board()
        if self.interactive:
            self.print_player_color()

    def play_demo(self):
        self._init_game()
        while not self.game_control.board.is_game_over():
            move = self.game_control.compute_best_move(10)
            self.game_control.apply_move(move[0])
            self.print_board()
        if self.interactive:
            self.print_scores()

    def print_scores(self):
        print("GameOver : {} moves. Result : {}"
              .format(self.game_control.nb_moves,
                      self.game_control.board.result()))

    def print_player_color(self):
        print(" ==> {} can move. =) (move <uci_move>)\n"
              .format("White"
                      if self.game_control.current_player.player.color
                      else "Black"))

    def quit(self):
        self.running = False


if __name__ == "__main__":
    try:
        pyarmchess = PyArmChess(interactive=True)
        pyarmchess.run()
    except Exception:
        print("Usage: pyarmchess_interactive")
