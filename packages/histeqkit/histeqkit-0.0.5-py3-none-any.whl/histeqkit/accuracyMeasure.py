import math
import numpy as np
from math import log2
import cv2
from skimage.metrics import structural_similarity as ssim


class accuracy:
    # Absolute Mean Brightness Error
    def AMBE(self, image_input, image_output):
        return abs(np.mean(image_input) - np.mean(image_output))

    # Mean Square Error
    def MSE(self, image_input, image_output):
        err = 10 * math.log10((255 * 255) / cv2.PSNR(image_input, image_output))
        return err

    # Peak Signal to Noise Ratio
    def PSNR(self, image_input, image_output):
        return cv2.PSNR(image_input, image_output)

    def SNR(self, image_input, image_output):
        ibg = 0
        signal = ((image_input + image_output) / 2 - ibg).sum()
        f = (0.5 ** 0.5) * ((2 / np.pi) ** -0.5)
        noise = np.abs(image_input - image_output).sum() * f
        snr = signal / noise
        return snr

    def SSIM(self, image_input, image_output):
        return ssim(image_input, image_output, multichannel=True)

    def discrete_entropy(self, image_input):
        # Read the input image in grayscale
        img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)

        # Convert the image to a 1D array
        img_flat = img.flatten()

        # Calculate the probabilities of each intensity level
        levels, counts = np.unique(img_flat, return_counts=True)
        probabilities = counts / len(img_flat)

        # Calculate the entropy of the image
        entropy = 0
        for i in range(len(levels)):
            p_i = probabilities[i]
            entropy -= p_i * log2(p_i) if p_i != 0 else 0

        return entropy
