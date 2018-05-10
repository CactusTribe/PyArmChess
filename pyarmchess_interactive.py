"""Main class of the program.

Run this script to run the game and interact with a prompt.
"""
import time
from collections import OrderedDict

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
                         "demo": self.play_demo}
        self.logs = OrderedDict()
        self._init_game()
        self._init_chess_camera()

    def _init_game(self):
        self.log_text(" -> Create new chessboard ...")
        if self.interactive:
            print(self.get_last_log())
        self.player_1 = PlayerControl(Player("Foo", human=True))
        self.player_2 = PlayerControl(Player("Bar"))
        self.game_control = GameControl(self.player_1, self.player_2)

    def _init_chess_camera(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            input_cmd = input("$ ")
            try:
                input_raw = str(input_cmd).strip().split()
                args_cmd = input_raw[1::]
                self.execute_command(input_raw[0], *args_cmd)
            except Exception as exc:
                self.log_text(str(exc))
                print(exc)

    def execute_command(self, command, *args):
        if command in self.commands.keys():
            self.log_text(command + str(args))
            self.commands[command](*args)
        else:
            self.log_text(" -> Invalid command.")
            raise InvalidCommandException(" -> Invalid command.")

    def log_text(self, text):
        timestamp = int(time.time())
        self.logs[timestamp] = text

    def get_last_log(self):
        timestamp = list(self.logs.keys())[-1]
        return self.logs[timestamp]

    def print_board(self):
        self.log_text(str(self.game_control.board))
        if self.interactive:
            print(self.game_control.board)

    def set_move(self, uci_move):
        self.game_control.apply_move(uci_move)
        self.print_board()

    def play_demo(self):
        while not self.game_control.board.is_game_over():
            move = self.game_control.compute_best_move(10)
            self.game_control.apply_move(move[0])
            self.print_board()
        print("GameOver : {} moves.".format(self.game_control.nb_moves))

    def quit(self):
        self.running = False


if __name__ == "__main__":
    try:
        pyarmchess = PyArmChess(interactive=True)
        pyarmchess.run()
    except Exception:
        print("Usage: pyarmchess_interactive")
