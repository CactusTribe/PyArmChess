"""Player controler"""


class PlayerControl(object):
    """Interact with model"""

    def __init__(self, player):
        """PlayerControl initialisation."""
        self.player = player

    def win_game(self):
        if self.player.score:
            self.player.score += 10
        else:
            self.player.score = 10
