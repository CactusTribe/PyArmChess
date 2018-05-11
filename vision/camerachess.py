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
    DIR_SAMPLES, TRANSFORM_PATH, CALIB_PATH, BOARD_SIZE, RESCALE_RATIO)

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

    def save_frame(self, path, frame):
        cv2.imwrite(path, frame.img)

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

    def get_edged_frame(self):
        frame = self.get_frame()
        edged = self.canny(frame.img)
        return CameraFrame(edged)
