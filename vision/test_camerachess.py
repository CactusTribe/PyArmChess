# pylint: disable = protected-access
"""Tests of vision.CameraChess."""

import os
import unittest

from vision.camerachess import (
    CameraChess, CalibrationRequiredException)

from vision.constants import CALIB_PATH, TRANSFORM_PATH


class CameraChessTest(unittest.TestCase):
    """CameraChess test class."""

    def setUp(self):
        """Init tests."""
        self.camerachess = CameraChess()

    def test_init_samples(self):
        # CameraChess._init_samples creates the correct dict.
        self.assertEqual(self.camerachess.samples["empty"],
                         "vision/samples/empty.jpg")

    def test_get_chessboard_perspective_transform(self):
        # CameraChess.get_chessboard_perspective_transform raises
        # CalibrationRequiredException.
        os.remove(TRANSFORM_PATH)
        self.assertFalse(os.path.exists(TRANSFORM_PATH))
        with self.assertRaises(CalibrationRequiredException):
            self.camerachess.get_chessboard_perspective_transform()

    def test_calibration(self):
        # CameraChess.calibration create the calibration file.
        self.camerachess.calibration()
        self.assertTrue(os.path.exists(TRANSFORM_PATH))
        frame = self.camerachess.get_frame_from_file(
            self.camerachess.samples["empty"])
        self.camerachess.save_frame(CALIB_PATH + "calibration.jpg", frame)
        self.assertTrue(os.path.exists(CALIB_PATH + "calibration.jpg"))
