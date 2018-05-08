"""Tests of game.PyArmChess."""

import unittest
import subprocess

from contextlib import contextmanager


class PyArmChessTest(unittest.TestCase):
    """PyArmChess test class."""

    def setUp(self):
        """Init tests."""
        pass

    @contextmanager
    def setup_with_subprocess(self):
        cmd = ["python3", "game/pyarmchess_interactive.py"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        yield process

    def send_input(self, input):
        with self.setup_with_subprocess() as process:
            output, err = process.communicate(
                input=input.encode("utf-8"))
            output = output.decode("utf-8").strip()
            return output, err

    def test_run_main(self):
        # PyArmChess runs without errors.
        output, _err = self.send_input("test Haha")
        output = output.split("\n")
        output = output[0].strip().replace("$ ", "")
        self.assertEqual(output, "Haha")

    def test_invalid_command(self):
        # PyArmChess  raises InvalidCommandException.
        output, err = self.send_input("invalid")
        output = output.split("\n")
        output = output[0].strip().replace("$ ", "")
        self.assertEqual(output, " -> Invalid command.")
