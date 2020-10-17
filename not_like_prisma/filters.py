import math

import cv2
from pandas import np
from pywin.Demos import progressbar
import progressbar

import not_like_prisma.utils

from not_like_prisma.vector_field import VectorField
from not_like_prisma.color_palette import ColorPalette
from not_like_prisma.color_math import color_select, randomized_grid, compute_color_probabilities


class ImageFilters:

    def __init__(self, image):
        self.image = image

    def gray_filter(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def threshold_filter(self):
        _, th1 = cv2.threshold(self.image, 127, 255, cv2.THRESH_TOZERO_INV)
        return th1

    def increase_brightness(self, value=300):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def blur_filter(self):
        blur_image = cv2.blur(self.image, (9, 9), 0)
        return blur_image

    def sobel_filter(self):
        laplacian_image = cv2.Laplacian(self.image, cv2.CV_8U)
        return laplacian_image

    def sepia(self):
        img = self.image
        img = np.array(img, dtype=np.float64)
        img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                            [0.349, 0.686, 0.168],
                                            [0.393, 0.769, 0.189]]))
        img[np.where(img > 255)] = 255
        img = np.array(img, dtype=np.uint8)
        return img

    def cartoon(self):
        img = self.image
        edges1 = cv2.bitwise_not(cv2.Canny(img, 100, 200))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)
        dst = cv2.edgePreservingFilter(img, flags=2, sigma_s=64,
                                       sigma_r=0.25)
        cartoon1 = cv2.bitwise_and(dst, dst, mask=edges1)
        cartoon2 = cv2.bitwise_and(dst, dst, mask=edges2)
        return cartoon2

    def pencil_scatch(self):
        img = self.image
        dst_gray, dst_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return dst_color

    def pointillism(self):
        img = self.image
        limit_image_size = 0
        if limit_image_size > 0:
            img = not_like_prisma.limit_size(img, limit_image_size)
        stroke_scale = 0
        if stroke_scale == 0:
            stroke_scale = int(math.ceil(max(img.shape) / 1000))
        else:
            stroke_scale = stroke_scale
        gradient_smoothing_radius = 0
        if gradient_smoothing_radius == 0:
            gradient_smoothing_radius = int(round(max(img.shape) / 50))
        else:
            gradient_smoothing_radius = gradient_smoothing_radius
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        palette_size = 20
        palette = ColorPalette.from_image(img, palette_size)
        palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
        cv2.imshow("palette", palette.to_image())
        cv2.waitKey(200)
        gradient = VectorField.from_gradient(gray)
        gradient.smooth(gradient_smoothing_radius)
        res = cv2.medianBlur(img, 11)
        grid = randomized_grid(img.shape[0], img.shape[1], scale=3)
        batch_size = 10000
        bar = progressbar.ProgressBar()
        for h in bar(range(0, len(grid), batch_size)):
            pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
            color_probabilities = compute_color_probabilities(pixels, palette, k=9)
            for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
                color = color_select(color_probabilities[i], palette)
                angle = math.degrees(gradient.direction(y, x)) + 90
                length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))
                cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)
        return res
