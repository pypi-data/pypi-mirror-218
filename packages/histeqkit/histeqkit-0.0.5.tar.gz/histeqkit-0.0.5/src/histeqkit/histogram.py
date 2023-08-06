import math
import cv2
import time
import numpy as np
from skimage.exposure import histogram


class Histogram:

    def tanh_func(self,x):
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    def find_k_opt(self,pdf_x, lower, upper, mode):
        max_variance = -float('inf')
        k_opt = 0
        r_lower = 0
        r_upper = 0

        if mode == 'u':
            r_lower = -lower
            r_upper = -lower
        else:
            r_lower = 0
            r_upper = 0

        for i in range(lower, upper - 1):
            omega_0 = sum(pdf_x[lower + r_lower + 1: i + r_lower + 1])
            omega_1 = sum(pdf_x[i + r_lower + 2: upper + r_lower])
            mu_0 = 0
            if not (omega_0 == 0 or omega_1 == 0):
                for j in range(lower, i + 1):
                    if j + r_lower + 1 >= len(pdf_x):
                        break
                    mu_0 += (j * pdf_x[j + r_lower + 1]) / omega_0
                mu_1 = 0
                for j in range(i + 1, upper - 1):
                    if j + r_lower + 1 >= len(pdf_x):
                        break
                    mu_1 += (j * pdf_x[j + r_lower + 1]) / omega_1
                mu = (mu_0 * omega_0) + (mu_1 * omega_1)
                var_x = omega_0 * (mu_0 - mu) ** 2 + omega_1 * (mu_1 - mu) ** 2
                if var_x > max_variance:
                    max_variance = var_x
                    k_opt = i

        return k_opt

    def sub_histogram_equalization(self, histogram, range_min=0, range_max=255):
        cdf = histogram.cumsum()
        cdf_mask = np.ma.masked_equal(cdf, 0)

        # Scale cdf to [range_min, range_max]
        scale_cdf_mask = ((cdf_mask - cdf_mask.min()) * (range_max - range_min) / (
                    cdf_mask.max() - cdf_mask.min())) + range_min
        LUT = np.ma.filled(scale_cdf_mask, 0).astype('uint8')

        return LUT

    def histogram_equalization(self, image_1d, range_min=0, range_max=255):
        histogram, _ = np.histogram(image_1d, range_max - range_min + 1, [range_min, range_max])

        return self.sub_histogram_equalization(histogram, range_min, range_max)

    def histogram_equalization_threshold(self, image_1d, threshold, start=0, end=255):
        lower_filter = image_1d <= threshold
        lower_1d = image_1d[lower_filter]

        upper_filter = image_1d > threshold
        upper_1d = image_1d[upper_filter]

        lower_input_lut = np.array([])
        if start > 0:
            for i in range(0, start):
                lower_input_lut = np.append(lower_input_lut, i)

        upper_input_lut = np.array([])
        if end < 255:
            for i in range(end + 1, 256):
                upper_input_lut = np.append(upper_input_lut, i)

        lower_LUT = self.histogram_equalization(lower_1d, start, threshold)
        upper_LUT = self.histogram_equalization(upper_1d, threshold + 1, end)

        lower_LUT = np.concatenate((lower_input_lut, lower_LUT))
        upper_LUT = np.concatenate((upper_LUT, upper_input_lut))

        LUT = np.concatenate((lower_LUT, upper_LUT))

        return LUT

    def histogram_equalization_recursively(self, image_1d, separate_func, recursive, start=0, end=255):
        if recursive > 0:
            separate = separate_func(image_1d)
            separate = math.floor(separate)

            lower_filter = image_1d <= separate
            lower_1d = image_1d[lower_filter]

            lower_equalization = self.histogram_equalization_recursively(lower_1d, separate_func, recursive - 1, start,
                                                                         separate)

            upper_filter = image_1d > separate
            upper_1d = image_1d[upper_filter]

            upper_equalization = self.histogram_equalization_recursively(upper_1d, separate_func, recursive - 1,
                                                                         separate + 1, end)

            return np.concatenate((lower_equalization, upper_equalization))
        else:
            return self.histogram_equalization(image_1d, start, end)