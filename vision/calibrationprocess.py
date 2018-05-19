"""Functions camera calibration"""

from itertools import product

import cv2
import numpy as np

from scipy.spatial.distance import euclidean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from vision.exceptions import (
    ChessBoardNotFoundException, CameraNotCenteredException)


class CalibrationProcess(object):
    """Use theses function to calibrate the camera."""

    def find_chessboard(self, frame):
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

    def predict_transform(self, chessboard):
        x_train = np.array(list(product(np.linspace(-3, 3, 7),
                                        np.linspace(-3, 3, 7))))
        poly = PolynomialFeatures(degree=4)
        x_train = poly.fit_transform(x_train)
        m_x = LinearRegression()
        m_x.fit(x_train, chessboard[:, 0])
        m_y = LinearRegression()
        m_y.fit(x_train, chessboard[:, 1])
        return (m_x, m_y, poly)

    def compute_transformation(self, prediction):
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
        return M
