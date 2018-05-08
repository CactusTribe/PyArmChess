"""Main class of the program.

Run this script to run the game and interact with a prompt.
"""


class InvalidCommandException(Exception):
    """Invalid command exception."""
    pass


class PyArmChess(object):
    """PyArmChess definition."""

    def __init__(self):
        """Initialisation."""
        self.running = False
        self.commands = {"quit": self.quit,
                         "test": self.test}

    def run(self):
        self.running = True
        while self.running:
            input_cmd = input("$ ")
            try:
                input_raw = str(input_cmd).strip().split()
                args_cmd = input_raw[1::]
                if input_raw[0] in self.commands.keys():
                    self.commands[input_raw[0]](*args_cmd)
                else:
                    raise InvalidCommandException(" -> Invalid command.")
            except (ValueError, TypeError, InvalidCommandException) as exc:
                print(exc)

    def test(self, str):
        print(str)

    def quit(self):
        self.running = False


if __name__ == "__main__":
    try:
        pyarmchess = PyArmChess()
        pyarmchess.run()
    except Exception:
        print("Usage: pyarmchess_interactive")
