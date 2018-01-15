import numpy as np
import sys, time
import cv2
from ChessboardFrame import ChessboardFrame
from itertools import product
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.spatial.distance import euclidean
from constants import *

if RUN_ON_PI:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

class ChessCamera(object):
    def __init__(self, image):
        if RUN_ON_PI:
            self.camera = PiCamera()
            self.camera.resolution = (640,480)
            self.camera.iso = CAMERA_ISO
            self.camera.exposure_compensation = CAMERA_COMP
            time.sleep(1)
            g = self.camera.awb_gains
            self.camera.awb_mode = 'off'
            self.camera.awb_gains = g
            self.camera.exposure_mode = 'off'

        self.IMAGE_PATH = image


    def get_frame(self):
        rawCapture = PiRGBArray(self.camera)
        self.camera.capture(rawCapture, format="bgr")
        return rawCapture.array

    def _chessboard_perspective_transform_path(self):
        return ('chessboard_perspective_transform.npy')

    def get_chessboard_perspective_transform(self):
        try:
            M = np.load(self._chessboard_perspective_transform_path())
            return M
        except IOError:
            print("No chessboard perspective transform found. Camera position recalibration required.")

    def calibration(self):
        if RUN_ON_PI:
            frame = self.get_frame()
        else:
            frame = cv2.imread(self.IMAGE_PATH)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        board_size = (7,7)
        found, corners = cv2.findChessboardCorners(frame, board_size, flags=cv2.CALIB_CB_NORMALIZE_IMAGE|cv2.CALIB_CB_ADAPTIVE_THRESH)
        assert found, "Couldn't find chessboard."

        z = corners.reshape((49,2))
        board_center = z[24]
        frame_center = frame.shape[1] / 2.0, frame.shape[0] / 2.0
        #assert euclidean(board_center, frame_center) < 40.0, "Camera is not centered over chessboard."

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

        if DEBUG:
            calib = self.current_board_frame()
            cv2.imwrite("calibration.jpg", calib.img)

    def current_board_frame(self):
        if RUN_ON_PI:
            frame = self.get_frame()
        else:
            frame = cv2.imread(self.IMAGE_PATH)

        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        M = self.get_chessboard_perspective_transform()
        frame = cv2.warpPerspective(frame, M, (BOARD_SIZE,BOARD_SIZE))

        #RESCALE
        height, width = frame.shape[:2]
        image_center = (BOARD_SIZE / 2, BOARD_SIZE / 2)
        img_scaled = cv2.resize(frame, (0,0), fx = RESCALE_RATIO, fy = RESCALE_RATIO)
        offset_h = int(((height * RESCALE_RATIO) - height)/2)
        offset_w = int(((width * RESCALE_RATIO) - width)/2)

        frame = img_scaled[offset_h:(height+offset_h), offset_w:(width+offset_w)]
        return ChessboardFrame(frame)

    def current_board_edged(self):
        frame = self.current_board_frame()
        edged = self.canny(frame.img)
        return ChessboardFrame(edged)

    def current_board_processed(self):
        edged = self.current_board_edged()
        current = self.current_board_frame()

        current.img = cv2.cvtColor(current.img, cv2.COLOR_BGR2GRAY)
        current.img = cv2.bilateralFilter(current.img, CANNY_BLUR, 17, 17)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(10,10))
        #current.img = clahe.apply(current.img)
        current.img = cv2.equalizeHist(current.img)

        if DEBUG : cv2.imwrite("output/edged.jpg", edged.img)

        board = []
        for i in range(8):
            line = []
            for j in range(8):
                edged_square = edged.square_at(j,i)

                if cv2.countNonZero(edged_square.img) > THRESHOLD_PRESENCE :
                    current_square = current.square_at(j,i)

                    masked, masked_draw = self.mask(current_square.img, edged_square.img)
                    thres = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

                    #masked_draw = self.adjust_gamma(masked, 1)
                    #masked_draw = self.adjust_gamma(masked_draw, 2)

                    #thres = self.adjust_gamma(thres, 0.5)
                    thres = cv2.GaussianBlur(thres, (13,13), 0)
                    _, thres = cv2.threshold(thres, THRESHOLD_BINARY, 255, cv2.THRESH_BINARY)

                    if DEBUG and MASK_DRAW:
                        cv2.imwrite("output/squares/{}.jpg".format(current_square.position), masked_draw)
                    if DEBUG and not MASK_DRAW:
                        cv2.imwrite("output/squares/{}.jpg".format(current_square.position), thres)

                    if cv2.countNonZero(thres) > THRESHOLD_COLOR :
                        line.append("W")
                    else:
                        line.append("B")
                else:
                    line.append(".")
            board.append(line)
        return board

    def canny(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = self.adjust_gamma(img, CANNY_GAMMA)

        kernel_sharpen = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        clahe = cv2.createCLAHE(clipLimit=CLAHE_LIMIT, tileGridSize=(CLAHE_GRID,CLAHE_GRID))

        img = clahe.apply(img)

        #img = cv2.normalize(img, img, alpha=50, beta=200, norm_type=cv2.NORM_MINMAX)
        img = cv2.bilateralFilter(img, CANNY_BLUR, 17, 17)
        #img = clahe.apply(img)
        #img = cv2.filter2D(img, -1, kernel_sharpen)
        #img = cv2.GaussianBlur(img, (CANNY_BLUR,CANNY_BLUR), 0)

        if DEBUG : cv2.imwrite("output/gray.jpg", img)

        edged = cv2.Canny(img, CANNY_LOWER, CANNY_UPPER)
        #edged = self.auto_canny(img, CANNY_SIGMA)

        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,(EDGE_DILATE,EDGE_DILATE))
        kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT,(EDGE_ERODE,EDGE_ERODE))
        #edged = cv2.dilate(edged, kernel_dilate)
        #edged = cv2.erode(edged, kernel_erode)
        edged = cv2.dilate(edged, None)
        edged = cv2.erode(edged, None)
        return edged

    def mask(self, img, edges):
        image, contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # Find largest contour
        max_perimetre = 0.0
        max_contour = None
        for c in contours:
            perimetre = cv2.arcLength(c, False)
            if perimetre >= max_perimetre:
                max_perimetre = perimetre
                max_contour = c

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        mask = np.zeros(edges.shape)
        hull = cv2.convexHull(max_contour)
        cv2.fillConvexPoly(mask, hull, (255))

        #-- Smooth mask, then blur it --------------------------------------------------------
        mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
        mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
        mask = cv2.GaussianBlur(mask, (MASK_BLUR, MASK_BLUR), 0)
        mask_stack = np.dstack([mask]*3)  # Create 3-channel alpha mask

        #-- Blend masked img into MASK_COLOR background --------------------------------------
        mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices,
        img         = img.astype('float32') / 255.0                 #  for easy blending

        masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
        masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit

        if MASK_DRAW:
            masked_draw = cv2.drawContours(masked.copy(), [hull], 0, (0,255,0), 2, cv2.LINE_AA, maxLevel=1)
        else: masked_draw = None

        return masked, masked_draw

    def adjust_gamma(self, image, gamma=1.0):
    	invGamma = 1.0 / gamma
    	table = np.array([((i / 255.0) ** invGamma) * 255
    		for i in np.arange(0, 256)]).astype("uint8")
    	return cv2.LUT(image, table)

    def auto_canny(self,image, sigma=0.33):
    	# compute the median of the single channel pixel intensities
    	v = np.median(image)

    	# apply automatic Canny edge detection using the computed median
    	lower = int(max(0, (1.0 - sigma) * v))
    	upper = int(min(255, (1.0 + sigma) * v))
    	edged = cv2.Canny(image, lower, upper)

    	# return the edged image
    	return edged
