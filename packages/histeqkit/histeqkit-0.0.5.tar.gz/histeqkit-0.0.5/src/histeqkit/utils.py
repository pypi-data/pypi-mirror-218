import math
import cv2
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


class Utils:
    def __init__(self, image, color_space='HSV'):
        self.image = image
        self.color_space = color_space

    def image_gray(self):
        if (self.color_space == 'HSV'):
            image_hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
            self.image_color = image_hsv

            return image_hsv[:, :, 2]
        elif self.color_space == 'Gray':
            image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
            self.image_color = image_gray

            return image_gray
        else:
            self.image_color = self.image
            return self.image

    def LUT_image(self, LUT):
        if (self.color_space == 'HSV'):
            for i in range(0, len(self.image_color)):
                for j in range(0, len(self.image_color[0])):
                    self.image_color[i][j][2] = LUT[self.image_color[i][j][2]]

            return cv.cvtColor(self.image_color, cv.COLOR_HSV2BGR)
        elif (self.color_space == 'Gray'):
            return LUT[self.image_color]
        else:
            return self.image_color

    def is_gray_image(self):
        blue, green, red = cv2.split(self.image)

        difference_red_green = np.count_nonzero(abs(red - green))
        difference_green_blue = np.count_nonzero(abs(green - blue))
        difference_blue_red = np.count_nonzero(abs(blue - red))

        difference_sum = float(difference_red_green + difference_green_blue + difference_blue_red)

        ratio = difference_sum / self.image.size

        if ratio > 0.005:
            return False
        else:
            return True

    def minimum_mean_brightness_error(self, image_1d):
        length = len(image_1d)

        unique_1d = np.unique(image_1d)
        max_1d = len(unique_1d)

        histogram, _ = np.histogram(image_1d, 256, [0, 255])

        mean = 0
        for i in range(0, len(unique_1d)):
            mean += i * histogram[unique_1d[i]]

        smbe = max_1d * (length - histogram[unique_1d[0]]) - 2 * mean
        asmbe = abs(smbe)
        position = 0
        for i in range(1, len(unique_1d)):
            smbe += (length - max_1d * histogram[unique_1d[i]])
            if asmbe > abs(smbe):
                asmbe = abs(smbe)
                position = i

        return unique_1d[position]
