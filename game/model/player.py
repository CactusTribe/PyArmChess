"""Description of the Player object."""


class Player(object):
    """Description."""

    def __init__(self, name, human=False):
        """Player initialisation."""
        self.name = name
        self.human = human
        self.score = None
