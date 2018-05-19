"""CameraChess module.

"""
import os
import platform
import time

import cv2
import numpy as np

from vision.cameraframe import CameraFrame
from vision.calibrationprocess import CalibrationProcess
from vision.imageprocess import ImageProcess

from vision.constants import (
    CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_ISO, CAMERA_COMP, CAMERA_BRIGHTNESS,
    DIR_SAMPLES, TRANSFORM_PATH, BOARD_SIZE, RESCALE_RATIO,
    THRESHOLD_PRESENCE, THRESHOLD_COLOR)

from vision.exceptions import (
    CalibrationRequiredException, SampleNotFoundException,
    PicameraNotFoundException)

if platform.machine() == 'armv7l':
    from picamera import PiCamera
    from picamera.array import PiRGBArray


class CameraChess(object):
    """CameraChess definition."""

    def __init__(self, run_on_rasp=False):
        """Initialisation."""
        self.run_on_rasp = run_on_rasp
        self.calibration_process = CalibrationProcess()
        self.image_process = ImageProcess()
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

    def calibration(self):
        """Compute the transformation matrice.

        With the empty board sample or frame from camera if run on rasp.
        """
        try:
            if self.run_on_rasp:
                frame = self.get_raw_frame()
            else:
                frame = cv2.imread(self.samples["empty"])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except NameError:
            raise PicameraNotFoundException("Can't found picamera module.")
        except cv2.error:
            raise SampleNotFoundException(
                "Unable to find empty sample for the calibration.")

        chessboard = self.calibration_process.find_chessboard(frame)
        prediction = self.calibration_process.predict_transform(chessboard)
        matrice = self.calibration_process.compute_transformation(prediction)
        np.save(self._chessboard_perspective_transform_path(), matrice)

    def get_raw_frame(self):
        """Return a raw image in bgr format from camera."""
        raw_capture = PiRGBArray(self.camera)
        self.camera.capture(raw_capture, format="bgr")
        return raw_capture.array

    def _compute_frame(self, frame):
        matrice = self.get_chessboard_perspective_transform()
        frame = cv2.warpPerspective(frame, matrice, (BOARD_SIZE, BOARD_SIZE))
        # RESCALE
        height, width = frame.shape[:2]
        img_scaled = cv2.resize(frame, (0, 0),
                                fx=RESCALE_RATIO, fy=RESCALE_RATIO)
        offset_h = int(((height * RESCALE_RATIO) - height) / 2)
        offset_w = int(((width * RESCALE_RATIO) - width) / 2)
        frame = img_scaled[offset_h:(height + offset_h),
                           offset_w:(width + offset_w)]
        return CameraFrame(frame)

    def get_frame(self):
        frame = self.get_raw_frame()
        return self._compute_frame(frame)

    def get_frame_from_file(self, file_image):
        frame = cv2.imread(file_image)
        return self._compute_frame(frame)

    def get_edged_frame(self, *args):
        if self.run_on_rasp:
            frame = self.get_frame()
        else:
            frame = self.get_frame_from_file(args[0])
        edged = self.image_process.canny(frame.image)
        return CameraFrame(edged)

    def get_processed_frame(self, *args):
        if self.run_on_rasp:
            current = self.get_frame()
        else:
            current = self.get_frame_from_file(args[0])
        edged = self.get_edged_frame(*args)
        current.image = self.image_process.preprocess_mask(current.image)
        edged_square_list = [
            edged.square_at(j, i) for i in range(8) for j in range(8)]
        current_square_list = [
            current.square_at(j, i) for i in range(8) for j in range(8)]
        board = []
        for (current_square, edged_square) in \
                zip(current_square_list, edged_square_list):
            board.append(
                self.get_piece_on_square(current_square, edged_square))
        return board

    def get_piece_on_square(self, current_square, edged_square):
        if cv2.countNonZero(edged_square.image) > THRESHOLD_PRESENCE:
            masked, _masked_draw = self.image_process.mask(
                current_square.image, edged_square.image)
            threshold = self.image_process.threshold(masked)
            height, width = threshold.shape
            count_white = cv2.countNonZero(threshold)
            count_black = height * width - count_white
            if count_black > THRESHOLD_COLOR:
                return "B"
            return "W"
        else:
            return "."

    def capture_move(self):
        frame_1 = self.get_processed_frame(
            self.samples["board1"])
        frame_2 = self.get_processed_frame(
            self.samples["board2"])
        return self._detect_move(frame_1, frame_2)

    def _detect_move(self, board_1, board_2):
        if not board_1 or not board_2:
            return ""
        old_position = None
        new_position = None
        print("## Compute next move...")
        for row in range(8):
            line_b1 = "".join(board_1[row])
            line_b2 = "".join(board_2[row])
            line_diff = [(str(chr(97 + col)), 8 - row)
                         for col in range(len(line_b1))
                         if line_b1[col] != line_b2[col]]
            if line_diff != []:
                fst_diff = line_diff[0]
                if line_b2[ord(fst_diff[0]) - 97] == ".":
                    old_position = "{}{}".format(fst_diff[0], fst_diff[1])
                else:
                    new_position = "{}{}".format(fst_diff[0], fst_diff[1])
        return "{}{}".format(old_position, new_position)
