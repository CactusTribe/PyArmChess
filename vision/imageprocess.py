"""Functions camera image processing"""

import cv2
import numpy as np

from vision.constants import (
    CANNY_BLUR, CANNY_LOWER, CANNY_UPPER, MASK_DILATE_ITER,
    MASK_ERODE_ITER, MASK_BLUR, THRESHOLD_BINARY)


class ImageProcess(object):
    """Use theses function to process images."""

    def adjust_gamma(self, image, gamma=1.0):
        inv_gamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** inv_gamma) * 255
             for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def auto_canny(self, image, sigma=0.33):
        # Compute the median of the single channel pixel intensities.
        median = np.median(image)
        # Apply automatic Canny edge detection using the computed median.
        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))
        edged = cv2.Canny(image, lower, upper)
        return edged

    def preprocess_canny(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # img = cv2.GaussianBlur(img, (CANNY_BLUR,CANNY_BLUR), 0)
        image = cv2.bilateralFilter(image, CANNY_BLUR, 17, 17)
        kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        image = cv2.filter2D(image, -1, kernel_sharpen)
        return image

    def canny(self, image):
        """Apply the canny filter to the image."""
        image = self.preprocess_canny(image)
        edged = cv2.Canny(image, CANNY_LOWER, CANNY_UPPER)
        # edged = self.auto_canny(img, CANNY_SIGMA)
        edged = cv2.dilate(edged, None)
        edged = cv2.erode(edged, None)
        return edged

    def preprocess_mask(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.bilateralFilter(image, 13, 17, 17)
        image = cv2.equalizeHist(image)
        return image

    def mask(self, image, edges):
        max_contour = self.find_max_contours(edges)
        mask = np.zeros(edges.shape, dtype=np.uint8)
        hull = cv2.convexHull(max_contour)
        cv2.fillConvexPoly(mask, hull, (255))
        background = np.full(image.shape, 255, dtype=np.uint8)
        # get masked foreground
        fg_masked = cv2.bitwise_and(image, image, mask=mask)
        # get masked background, mask must be inverted
        mask = cv2.bitwise_not(mask)
        mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
        mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
        mask = cv2.GaussianBlur(mask, (MASK_BLUR, MASK_BLUR), 0)
        bk_masked = cv2.bitwise_and(background, background, mask=mask)
        # combine masked foreground and masked background
        masked = cv2.bitwise_or(fg_masked, bk_masked)
        masked_draw = self.draw_contours(masked, hull)
        return masked, masked_draw

    def find_max_contours(self, edged):
        _img, contours, _hierarchy = cv2.findContours(
            edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # Find largest contour
        max_perimetre = 0.0
        max_contour = None
        for contour in contours:
            perimetre = cv2.arcLength(contour, False)
            if perimetre >= max_perimetre:
                max_perimetre = perimetre
                max_contour = contour
        return max_contour

    def draw_contours(self, masked, convex_hull):
        masked = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
        masked_draw = cv2.drawContours(
            masked.copy(), [convex_hull], 0,
            (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)
        return masked_draw

    def threshold(self, masked):
        _, thres = cv2.threshold(masked, THRESHOLD_BINARY,
                                 255, cv2.THRESH_BINARY)
        return thres

    def save_image(self, path, image):
        cv2.imwrite(path, image)
