DEBUG = False
RUN_ON_PI = False

# BOARD CONSTANTS
SQUARE_SIZE = 60
BOARD_SIZE = SQUARE_SIZE * 8

# IMAGE PROCESS
RESCALE_RATIO = 1.015

CANNY_LOWER = 40
CANNY_UPPER = 50
CANNY_BLUR = 7
CANNY_GAMMA = 1.5

MASK_BLUR = 21
MASK_DILATE_ITER = 2
MASK_ERODE_ITER = 8
MASK_COLOR = (0,0,0)
MASK_DILATE = 13

THRESHOLD_PRESENCE = 50
THRESHOLD_COLOR = 300
THRESHOLD_BINARY = 90
