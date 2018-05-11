"""CameraChess module.

"""
import os
import platform
import time

from itertools import product

import cv2
import numpy as np

from scipy.spatial.distance import euclidean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from vision.constants import (
    CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_ISO, CAMERA_COMP, CAMERA_BRIGHTNESS,
    DIR_SAMPLES, TRANSFORM_PATH)

from vision.exceptions import (
    CalibrationRequiredException, SampleNotFoundException,
    PicameraNotFoundException, ChessBoardNotFoundException,
    CameraNotCenteredException)

if platform.machine() == 'armv7l':
    from picamera import PiCamera
    from picamera.array import PiRGBArray


class CameraChess(object):
    """CameraChess definition."""

    def __init__(self, run_on_rasp=False):
        """Initialisation."""
        self.run_on_rasp = run_on_rasp
        if self.run_on_rasp:
            try:
                self._init_picamera()
            except NameError:
                raise PicameraNotFoundException(
                    "Can't found picamera module.")
        else:
            self._init_samples()

    def _init_picamera(self):
        self.camera = PiCamera()
        self.camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        self.camera.iso = CAMERA_ISO
        self.camera.exposure_compensation = CAMERA_COMP
        self.camera.brightness = CAMERA_BRIGHTNESS
        time.sleep(1)  # Wait warming up.
        gain = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = gain
        self.camera.exposure_mode = 'off'

    def _init_samples(self):
        self.samples = {}
        for filename in os.listdir(DIR_SAMPLES):
            if filename.endswith(".jpg"):
                name = filename.split(".")[0]
                self.samples[name] = os.path.join(DIR_SAMPLES, filename)

    def _chessboard_perspective_transform_path(self):
        return (TRANSFORM_PATH)

    def get_chessboard_perspective_transform(self):
        try:
            matrice = np.load(self._chessboard_perspective_transform_path())
            return matrice
        except IOError:
            raise CalibrationRequiredException(
                " -> CameraChess: Camera position recalibration required.")

    def get_frame(self):
        """Return a raw image in bgr format from camera."""
        raw_capture = PiRGBArray(self.camera)
        self.camera.capture(raw_capture, format="bgr")
        return raw_capture.array

    def calibration(self):
        """Compute the transformation matrice.

        With the empty board sample or frame from camera if run on rasp.
        """
        try:
            if self.run_on_rasp:
                frame = self.get_frame()
            else:
                frame = cv2.imread(self.samples["empty"])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except NameError:
            raise PicameraNotFoundException("Can't found picamera module.")
        except cv2.error:
            raise SampleNotFoundException(
                "Unable to find empty sample for the calibration.")

        chessboard = self._find_chessboard(frame)
        prediction = self._predict_transformation(chessboard)
        self._compute_transformation(prediction)

    def _find_chessboard(self, frame):
        found, corners = cv2.findChessboardCorners(
            frame, (7, 7),
            flags=cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_ADAPTIVE_THRESH)
        if not found:
            raise ChessBoardNotFoundException()
        reshape = corners.reshape((49, 2))
        board_center = reshape[24]
        frame_center = frame.shape[1] / 2.0, frame.shape[0] / 2.0
        if euclidean(board_center, frame_center) < 10.0:
            raise CameraNotCenteredException()
        return reshape

    def _predict_transformation(self, chessboard):
        x_train = np.array(list(product(np.linspace(-3, 3, 7),
                                        np.linspace(-3, 3, 7))))
        poly = PolynomialFeatures(degree=4)
        x_train = poly.fit_transform(x_train)
        m_x = LinearRegression()
        m_x.fit(x_train, chessboard[:, 0])
        m_y = LinearRegression()
        m_y.fit(x_train, chessboard[:, 1])
        return (m_x, m_y, poly)

    def _compute_transformation(self, prediction):
        # pylint: disable = invalid-name
        m_x = prediction[0]
        m_y = prediction[1]
        poly = prediction[2]

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
