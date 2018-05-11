# pylint: disable = protected-access
"""Tests of vision.CameraChess."""

import os
import unittest

from vision.camerachess import (
    CameraChess, CalibrationRequiredException)

from vision.constants import CALIB_PATH, PROCESSED_PATH, TRANSFORM_PATH


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
        self.camerachess.image_process.save_image(
            CALIB_PATH + "calibration.jpg", frame.image)
        self.assertTrue(os.path.exists(CALIB_PATH + "calibration.jpg"))

    def test_get_edged(self):
        # CameraChess.get_edged_frame create the edged file.
        self.camerachess.calibration()
        frame = self.camerachess.get_edged_frame(
            self.camerachess.samples["board1"])
        self.camerachess.image_process.save_image(
            PROCESSED_PATH + "edged.jpg", frame.image)
        self.assertTrue(os.path.exists(PROCESSED_PATH + "edged.jpg"))

    def test_get_processed_frame(self):
        # CameraChess.get_processed_frame create all processing files.
        # if DEBUG and MASK_DRAW:
        #     cv2.imwrite("output/squares/{}.jpg".format(current_square.position), masked_draw)
        # if DEBUG and not MASK_DRAW:
        #     cv2.imwrite("output/squares/{}.jpg".format(current_square.position), thres)
        self.camerachess.calibration()
        frame = self.camerachess.get_processed_frame(
            self.camerachess.samples["board1"])
        self.camerachess.image_process.save_image(
            PROCESSED_PATH + "edged.jpg", frame.image)
