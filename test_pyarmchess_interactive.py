"""Tests of game.PyArmChess."""

import unittest
import subprocess

from contextlib import contextmanager

from pyarmchess_interactive import InvalidCommandException, PyArmChess
from game.controler.gamecontrol import InvalidMoveException


class PyArmChessTest(unittest.TestCase):
    """PyArmChess test class."""

    def setUp(self):
        """Init tests."""
        self.pyarmchess = PyArmChess()

    @contextmanager
    def setup_with_subprocess(self):
        cmd = ["python3", "pyarmchess_interactive.py"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        yield process

    def send_input(self, input):
        with self.setup_with_subprocess() as process:
            output, err = process.communicate(
                input=input.encode("utf-8"))
            output = output.decode("utf-8").strip()
            return output, err

    def get_ouput(self):
        with self.setup_with_subprocess() as process:
            output = process.communicate()[0]
            output = output.decode("utf-8").strip()
            return output

    def test_run_main(self):
        # PyArmChess runs without errors.
        output = self.pyarmchess.get_last_log()
        self.assertEqual(output, " -> Create new chessboard ...")

    def test_invalid_command(self):
        # PyArmChess.execute_command raises InvalidCommandException.
        with self.assertRaises(InvalidCommandException):
            self.pyarmchess.execute_command("invalid", "blabla")

    def test_print_command(self):
        # PyArmChess.print_board prints the board.
        self.pyarmchess.execute_command("print")
        model = "r n b q k b n r\n" \
                "p p p p p p p p\n" \
                ". . . . . . . .\n" \
                ". . . . . . . .\n" \
                ". . . . . . . .\n" \
                ". . . . . . . .\n" \
                "P P P P P P P P\n" \
                "R N B Q K B N R"
        board = self.pyarmchess.get_last_log()
        self.assertEqual(model, board)

    def test_move_command(self):
        # PyArmChess.move applies the movement.
        self.pyarmchess.execute_command("move", "e2e4")
        model = "r n b q k b n r\n" \
                "p p p p p p p p\n" \
                ". . . . . . . .\n" \
                ". . . . . . . .\n" \
                ". . . . P . . .\n" \
                ". . . . . . . .\n" \
                "P P P P . P P P\n" \
                "R N B Q K B N R"
        board = self.pyarmchess.get_last_log()
        self.assertEqual(model, board)

    def test_switch_player(self):
        # PyArmChess.move switchs current_player.
        self.pyarmchess.execute_command("move", "e2e4")
        self.pyarmchess.execute_command("move", "e7e5")
        model = "r n b q k b n r\n" \
                "p p p p . p p p\n" \
                ". . . . . . . .\n" \
                ". . . . p . . .\n" \
                ". . . . P . . .\n" \
                ". . . . . . . .\n" \
                "P P P P . P P P\n" \
                "R N B Q K B N R"
        board = self.pyarmchess.get_last_log()
        self.assertEqual(model, board)

    def test_invalid_move(self):
        # PyArmChess.move raises InvalidMoveException.
        with self.assertRaises(InvalidMoveException):
            self.pyarmchess.execute_command("move", "e8e4")

    def test_play_demo(self):
        # PyArmChess.play_demo does the right scenario.
        move = self.pyarmchess.game_control.compute_best_move(10)
        self.pyarmchess.game_control.apply_move(move[0])
        self.pyarmchess.execute_command("move", "e7e5")
