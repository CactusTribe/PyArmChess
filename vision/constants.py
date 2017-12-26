DEBUG = True
RUN_ON_PI = False

# BOARD CONSTANTS
SQUARE_SIZE = 60
BOARD_SIZE = SQUARE_SIZE * 8

CAMERA_ISO = 1600
CAMERA_COMP = 20

# IMAGE PROCESS
RESCALE_RATIO = 1.015

CANNY_SIGMA = 0.8
CANNY_LOWER = 80
CANNY_UPPER = 200
CANNY_BLUR = 13
CANNY_GAMMA = 1

CLAHE_LIMIT = 1.0
CLAHE_GRID = 8

EDGE_DILATE = 6
EDGE_ERODE = 6

MASK_DRAW = False
MASK_BLUR = 11
MASK_DILATE = 9
MASK_DILATE_ITER = 1
MASK_ERODE_ITER = 3
MASK_COLOR = (0,0,0)

THRESHOLD_PRESENCE = 80
THRESHOLD_COLOR = 100
THRESHOLD_BINARY = 100
