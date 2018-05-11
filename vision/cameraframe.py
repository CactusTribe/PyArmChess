from vision.Square import Square
from vision.constants import SQUARE_SIZE


class CameraFrame(object):
    def __init__(self, img):
        self.img = img

    def square_at(self, pos_x, pos_y):
        position = "{}{}".format(chr(97 + pos_x), 8 - pos_y)
        pos_y = pos_y * SQUARE_SIZE
        pos_x = pos_x * SQUARE_SIZE
        img = self.img[pos_y:pos_y+SQUARE_SIZE, pos_x:pos_x+SQUARE_SIZE]
        cropped = img[5:55, 5:55]
        return Square(position, cropped)
