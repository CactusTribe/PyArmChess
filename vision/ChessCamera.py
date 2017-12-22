import numpy as np
import sys
import cv2
from ChessboardFrame import ChessboardFrame
from itertools import product
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.spatial.distance import euclidean
from constants import SQUARE_SIZE, BOARD_SIZE

class ChessCamera(object):
    def __init__(self):
        pass

    def _chessboard_perspective_transform_path(self):
        return ('chessboard_perspective_transform.npy')

    def get_chessboard_perspective_transform(self):
        try:
            M = np.load(self._chessboard_perspective_transform_path())
            return M
        except IOError:
            print("No chessboard perspective transform found. Camera position recalibration required.")

    def calibration(self, img):
        board_size = (7,7)
        #_, frame = cv2.VideoCapture(0).read()
        frame = cv2.imread(img)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(frame, board_size, flags=cv2.CALIB_CB_NORMALIZE_IMAGE|cv2.CALIB_CB_ADAPTIVE_THRESH)

        assert found, "Couldn't find chessboard."

        z = corners.reshape((49,2))
        board_center = z[24]
        frame_center = frame.shape[1] / 2.0, frame.shape[0] / 2.0

        #assert euclidean(board_center, frame_center) < 20.0, "Camera is not centered over chessboard."

        X_train = np.array(list(product(np.linspace(-3, 3, 7), np.linspace(-3, 3, 7))))
        poly = PolynomialFeatures(degree=4)
        X_train = poly.fit_transform(X_train)

        m_x = LinearRegression()
        m_x.fit(X_train, z[:, 0])

        m_y = LinearRegression()
        m_y.fit(X_train, z[:, 1])

        def predict(i, j):
            features = poly.fit_transform(np.array([[i, j]]))
            return m_x.predict(features), m_y.predict(features)

        P = []
        Q = []

        x, y = predict(4.0, 4.0)
        P.append((x[0], y[0]))
        Q.append((0.0, 0.0))

        x, y = predict(-4.0, 4.0)
        P.append((x[0], y[0]))
        Q.append((0.0, 480.0))

        x, y = predict(4.0, -4.0)
        P.append((x[0], y[0]))
        Q.append((480.0, 0.0))

        x, y = predict(-4.0, -4.0)
        P.append((x[0], y[0]))
        Q.append((480.0, 480.0))

        Q = np.array(Q, np.float32)
        P = np.array(P, np.float32).reshape(Q.shape)

        M = cv2.getPerspectiveTransform(P, Q)
        np.save(self._chessboard_perspective_transform_path(), M)

    def current_board_frame(self):
        frame = cv2.imread(IMAGE_PATH)

        M = self.get_chessboard_perspective_transform()
        frame = cv2.warpPerspective(frame, M, (BOARD_SIZE,BOARD_SIZE))

        #RESCALE
        ratio = 1.015
        height, width = frame.shape[:2]
        image_center = (BOARD_SIZE / 2, BOARD_SIZE / 2)
        img_scaled = cv2.resize(frame, (0,0), fx=ratio, fy=ratio)
        offset_h = int(((height*ratio) - height)/2)
        offset_w = int(((width*ratio) - width)/2)
        frame = img_scaled[offset_h:(height+offset_h), offset_w:(width+offset_w)]

        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return ChessboardFrame(frame)

    def current_edged_board_frame(self):
        frame = cv2.imread(IMAGE_PATH)

        M = self.get_chessboard_perspective_transform()
        frame = cv2.warpPerspective(frame, M, (BOARD_SIZE,BOARD_SIZE))

        #RESCALE
        ratio = 1.015
        height, width = frame.shape[:2]
        image_center = (BOARD_SIZE / 2, BOARD_SIZE / 2)
        img_scaled = cv2.resize(frame, (0,0), fx=ratio, fy=ratio)
        offset_h = int(((height*ratio) - height)/2)
        offset_w = int(((width*ratio) - width)/2)
        frame = img_scaled[offset_h:(height+offset_h), offset_w:(width+offset_w)]
        edged = self.canny(frame)

        return ChessboardFrame(edged)

    def adjust_gamma(self, image, gamma=1.0):
    	invGamma = 1.0 / gamma
    	table = np.array([((i / 255.0) ** invGamma) * 255
    		for i in np.arange(0, 256)]).astype("uint8")

    	return cv2.LUT(image, table)

    def canny(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #img = self.adjust_gamma(img, 2)

        # EDGE DETECTION
        sigma=0.33
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        #kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        #img = cv2.filter2D(img, -1, kernel)

        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        img = clahe.apply(img)
        img = cv2.GaussianBlur(img, (5, 5), 3)

        #cv2.imwrite("output/inter_{}".format(image_path), img)

        edged = cv2.Canny(img, 50, 160)
        edged = cv2.dilate(edged, None)
        edged = cv2.erode(edged, None)
        return edged

def printBoard(board):
    for l in board:
        print(l)

def mask(img, edges):
    BLUR = 21
    MASK_DILATE_ITER = 2
    MASK_ERODE_ITER = 8
    MASK_COLOR = (0,0,0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(13,13))
    edges = cv2.dilate(edges, kernel)
    edges = cv2.erode(edges, None)

    image, contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find largest contour
    max_perimetre = 0.0
    max_contour = None
    for c in contours:
        perimetre = cv2.arcLength(c, False)
        if perimetre >= max_perimetre:
            max_perimetre = perimetre
            max_contour = c

    #masked = cv2.drawContours(img, [max_contour], 0, (0,255,0), 2, cv2.LINE_AA, maxLevel=1)

    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour, (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices,
    img         = img.astype('float32') / 255.0                 #  for easy blending

    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit
    #masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    return masked


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ChessCamera = ChessCamera()

        if "-c" in sys.argv:
            IMAGE_PATH = sys.argv[1]
            ChessCamera.calibration(IMAGE_PATH)
            current = ChessCamera.current_board_frame()
            cv2.imwrite("calibration.jpg", current.img)
        else:
            IMAGE_PATH = sys.argv[1]

            current = ChessCamera.current_board_frame()
            edged = ChessCamera.current_edged_board_frame()
            cv2.imwrite("output/edged.jpg", edged.img)

            # CUTTING SQUARES
            board = []
            threshold_piece = 50
            threshold_color = 300
            for i in range(8):
                line = []
                for j in range(8):
                    edged_square = edged.square_at(j,i)

                    if cv2.countNonZero(edged_square.img) > threshold_piece :

                        current_square = current.square_at(j,i)
                        masked = mask(current_square.img, edged_square.img)

                        masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
                        _, masked = cv2.threshold(masked,90,255,cv2.THRESH_BINARY)

                        cv2.imwrite("output/squares/{}.jpg".format(current_square.position), masked)
                        if cv2.countNonZero(masked) > threshold_color :
                            line.append("W")
                        else:
                            line.append("B")
                    else:
                        line.append(".")
                board.append(line)

            printBoard(board)

    else:
        print("Usage: ChessCamera <image> -c")
