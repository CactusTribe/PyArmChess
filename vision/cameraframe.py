from vision.square import Square
from vision.constants import SQUARE_SIZE


class CameraFrame(object):
    def __init__(self, image):
        self.image = image

    def square_at(self, pos_x, pos_y):
        position = "{}{}".format(chr(97 + pos_x), 8 - pos_y)
        pos_y = pos_y * SQUARE_SIZE
        pos_x = pos_x * SQUARE_SIZE
        image = self.image[pos_y:pos_y + SQUARE_SIZE, pos_x:pos_x + SQUARE_SIZE]
        cropped = image[5:55, 5:55]
        return Square(position, cropped)
