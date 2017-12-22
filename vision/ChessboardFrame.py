import numpy as np
from Square import Square
from constants import SQUARE_SIZE, BOARD_SIZE

class ChessboardFrame():
    def __init__(self, img):
        self.img = img

    def square_at(self, x, y):
        position = "{}{}".format(chr(97 + x), 8-y)
        y = y * SQUARE_SIZE
        x = x * SQUARE_SIZE
        img = self.img[y:y+SQUARE_SIZE, x:x+SQUARE_SIZE]
        cropped = img[5:55, 5:55]
        return Square(position, cropped)
