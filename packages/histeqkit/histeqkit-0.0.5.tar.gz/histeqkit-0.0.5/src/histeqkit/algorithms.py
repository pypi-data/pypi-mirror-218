import math
import numpy as np
import numpy.ma as ma
import cv2 as cv
import cv2
from .utils import Utils
from .histogram import Histogram
from skimage import exposure
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


class IE:
    def __init__(self, image, color_space='HSV'):
        self.image = image
        self.color_space = color_space

    ########################################
    #
    # Histogram equalization
    #
    ########################################

    # INVERT
    def INVERT(self):
        im = np.array(self.image)
        mask = np.full(im.shape, 255)
        mod_img = mask - im
        img_output = mod_img.astype(np.uint8)
        return img_output

    # CLAHE
    def CLAHE(self):
        image = self.image  # Read as grayscale
        # Create a CLAHE object
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # Apply CLAHE to the image
        clahe_image = clahe.apply(image)
        return clahe_image

    # #Gamma Correction
    def gammaCorrection(self):
        src = self.image
        gamma = 2
        invGamma = 1 / gamma
        table = [((i / 255) ** invGamma) * 255 for i in range(256)]
        table = np.array(table, np.uint8)
        return cv2.LUT(src, table)

    def AGC(self):
        image = self.image
        gamma = 1.0
        # Calculate the gamma correction lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype(np.uint8)

        # Split the image into color channels
        channels = cv2.split(image)

        # Apply gamma correction to each channel
        corrected_channels = []
        for channel in channels:
            corrected_channel = cv2.LUT(channel, table)
            corrected_channels.append(corrected_channel)

        # Merge the corrected channels back into an image
        corrected_image = cv2.merge(corrected_channels)

        return corrected_image

    def contrastStretching(self):
        img = self.image
        original = img.copy()
        xp = [0, 64, 128, 192, 255]
        fp = [0, 16, 128, 240, 255]
        x = np.arange(256)
        table = np.interp(x, xp, fp).astype('uint8')
        img = cv2.LUT(img, table)
        # cv2_imshow(original)
        return (img)

    def MVSIHE(self):
        histogram = Histogram()
        x = self.image
        b_delta = 0.6
        L = 256
        m, n = x.shape
        hist_x = np.histogram(x, bins=np.arange(L + 1))[0]
        pdf_x = hist_x / (m * n)
        k_op2 = histogram.find_k_opt(pdf_x, 0, L, 'g')

        h_sub_1 = hist_x[:k_op2 + 1]
        h_sub_2 = hist_x[k_op2 + 1:]

        pdf_sub_1 = h_sub_1 / h_sub_1.sum()
        pdf_sub_2 = h_sub_2 / h_sub_2.sum()
        k_op1 = histogram.find_k_opt(pdf_sub_1, 0, k_op2, 'l')
        k_op3 = histogram.find_k_opt(pdf_sub_2, k_op2 + 1, L, 'u')

        bounds1 = [0, k_op1]
        bounds2 = [k_op1, k_op2]
        bounds3 = [k_op2, k_op3]
        bounds4 = [k_op3, L - 1]
        # there, a few boundary fixes
        h_sub_1 = hist_x[bounds1[0]: bounds1[1] + 1]
        h_sub_2 = hist_x[bounds2[0] + 1: bounds2[1] + 1]
        h_sub_3 = hist_x[bounds3[0] + 1: bounds3[1] + 1]
        h_sub_4 = hist_x[bounds4[0] + 1: bounds4[1] + 1]

        pdf_sub_1 = h_sub_1 / h_sub_1.sum()
        pdf_sub_2 = h_sub_2 / h_sub_2.sum()
        pdf_sub_3 = h_sub_3 / h_sub_3.sum()
        pdf_sub_4 = h_sub_4 / h_sub_4.sum()

        new_pdf_sub_1 = histogram.tanh_func(pdf_sub_1)
        new_pdf_sub_1 = new_pdf_sub_1[:, ~np.all(new_pdf_sub_1 == 0, axis=0)]

        new_pdf_sub_2 = histogram.tanh_func(pdf_sub_2)
        new_pdf_sub_2 = new_pdf_sub_2[:, ~np.all(new_pdf_sub_2 == 0, axis=0)]

        new_pdf_sub_3 = histogram.tanh_func(pdf_sub_3)
        new_pdf_sub_3 = new_pdf_sub_3[:, ~np.all(new_pdf_sub_3 == 0, axis=0)]

        new_pdf_sub_4 = histogram.tanh_func(pdf_sub_4)
        new_pdf_sub_4 = new_pdf_sub_4[:, ~np.all(new_pdf_sub_4 == 0, axis=0)]

        cdf_sub_1 = np.matmul(new_pdf_sub_1.T, np.triu(np.ones((new_pdf_sub_1.shape[0], new_pdf_sub_1.shape[0]))))
        cdf_sub_2 = np.matmul(new_pdf_sub_2.T, np.triu(np.ones((new_pdf_sub_2.shape[0], new_pdf_sub_2.shape[0]))))
        cdf_sub_3 = np.matmul(new_pdf_sub_3.T, np.triu(np.ones((new_pdf_sub_3.shape[0], new_pdf_sub_3.shape[0]))))
        cdf_sub_4 = np.matmul(new_pdf_sub_4.T, np.triu(np.ones((new_pdf_sub_4.shape[0], new_pdf_sub_4.shape[0]))))

        # # histogram equilization method
        fx_sub_1 = (bounds1[0] + ((bounds1[1] - bounds1[0])) * cdf_sub_1).squeeze()
        fx_sub_2 = (bounds2[0] + ((bounds2[1] - bounds2[0])) * cdf_sub_2).squeeze()
        fx_sub_3 = (bounds3[0] + ((bounds3[1] - bounds3[0])) * cdf_sub_3).squeeze()
        fx_sub_4 = (bounds4[0] + ((bounds4[1] - bounds4[0])) * cdf_sub_4).squeeze()

        m, n = x.shape
        out = np.zeros((m, n), dtype=np.uint8)
        for i in range(L):
            if i <= bounds1[1]:
                out[x == i] = (fx_sub_1[i])
            elif bounds1[1] < i <= bounds2[1]:
                out[x == i] = fx_sub_2[i - bounds2[0] - 1]
            elif bounds2[1] < i <= bounds3[1]:
                out[x == i] = fx_sub_3[i - bounds3[0] - 1]
            elif bounds3[1] < i <= bounds4[1]:
                out[x == i] = fx_sub_4[i - bounds4[0] - 1]

        #############
        # # Normalisation Phase
        L_min = out.min()
        L_max = out.max()
        T_L = ((out.astype(float) - L_min) / (L_max - L_min)) * 255
        PCR_img = b_delta * T_L + (1 - b_delta) * x.astype(float)
        out = PCR_img.astype(np.uint8)

        out = np.array(out, dtype='uint8')  # converting out to a numpy array
        return (out)

    def ESIHE(self):
        data = self.image
        w = len(data)
        l1 = len(data[0])
        hist, bins = np.histogram(data.ravel(), 256, [0, 256])
        # print("Histogram of the image:")
        # print (hist) #Histogram of the image calculate

        # Step2, calculate Xa
        num = 0
        denum = 0
        l = len(hist)
        for i in range(1, l + 1):
            num += hist[i - 1] * i
            denum += hist[i - 1]

        # Step3 Clipping threshold and calculate clipping hstogram
        exposure = (1.0 / l) * (num / (1.0 * denum))
        xa = int(round(l * (1 - exposure)))
        # print("Exposure value:", exposure)
        # print("Threshold value:", xa)
        # print("l:",l)

        clipthreshold = 0

        s = 0
        for i in range(1, l + 1):
            s += hist[i - 1]
        clipthreshold = (1.0 / l) * s

        hist_c = []

        for i in range(1, l + 1):
            if (hist[i - 1] > clipthreshold):
                hist_c.append(clipthreshold)
            else:
                hist_c.append(hist[i - 1])

        # print("Clipped Histogram of the image:")
        # print (hist_c) #Clipped Histogram of the image
        # print("Rounded exp value:", int(round(xa)))
        # Step 4 Histogram Sub Division and Equalization
        undexp = []
        overexp = []
        underexp = hist[0:int(round(xa + 1))]
        overexp = hist[int(round(xa + 1)):l]

        nl = 0
        nu = 0

        for i in range(0, xa + 1):
            nl += hist_c[i]
        for i in range(xa + 1, l):
            nu += hist_c[i]

        pl = []
        pu = []
        for i in range(0, int(round(xa + 1))):
            # print(hist_c[i],"and", nl)
            pl.append(hist_c[i] / nl)

        for i in range(int(round(xa + 1)), l):
            pu.append(hist_c[i] / nu)
            # print(pu[i], ":::", i)

        # Get corresponding CDF
        cl = []
        cu = []

        cl.append(pl[0])
        print("len", len(pl))
        for r in range(1, len(pl)):
            cl.append(pl[r] + cl[r - 1])

        print("Length:", len(cl))
        cu.append(pu[0])
        for r in range(1, (len(pu))):
            cu.append(pu[r] + cu[r - 1])

        ESIHEoutput = [[0 for x in range(l1)] for y in range(w)]
        # print("row and col",w, "and",l1)

        # print("Data:",data[0])
        for r in range(0, w):
            for s in range(0, l1):
                if data[r][s] < (xa + 1):
                    # print(data[r][s])
                    f = xa * cl[data[r][s]]
                    # print("r",r,"s",s)
                    ESIHEoutput[r][s] = round(f)
                    # print("ESIHE", r," n ", s, ":",ESIHEoutput[r][s])
                else:
                    f = (xa + 1) + (255 - xa) * cu[(data[r][s] - (xa + 1))]
                    ESIHEoutput[r][s] = round(f)

        # print("\nRESULT:")

        # print("Output matrix:\n\n")
        final = np.asarray(ESIHEoutput)

        out = np.array(final, dtype='uint8')  # converting out to a numpy array
        return (out)

    def BPDHE(self):
        image = self.image
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        smoothed_hist = gaussian_filter(hist.flatten(), sigma=1)

        # Step 2: Detection of the location of local maximums
        maxima = np.where(
            np.r_[True, smoothed_hist[1:] > smoothed_hist[:-1]] & np.r_[smoothed_hist[:-1] > smoothed_hist[1:], True])[
            0]

        # Step 3: Map each partition into a new dynamic range
        ranges = np.split(maxima, len(maxima) // 2 + 1)
        new_ranges = [np.linspace(r[0], r[-1], num=256) for r in ranges]

        # Step 4: Equalize each partition independently
        equalized_image = np.zeros_like(image)
        for i, new_range in enumerate(new_ranges):
            mask = np.logical_and(image >= new_range[0], image <= new_range[-1])
            equalized_image[mask] = np.interp(image[mask], new_range, np.linspace(0, 255, num=256))

        # Step 5: Normalize the image brightness
        normalized_image = cv2.normalize(equalized_image, None, 0, 255, cv2.NORM_MINMAX)

        return normalized_image.astype(np.uint8)

    def MHE(self):
        image = self.image
        # Convert the input image to grayscale
        # image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        # Calculate the histogram of the image
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])

        # Calculate the cumulative distribution function (CDF) of the histogram
        cdf = hist.cumsum()

        # Calculate the modified cumulative distribution function (MCDF)
        mcdf = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())

        # Map the pixel values to their corresponding MCDF values
        equalized_image = np.interp(image.flatten(), bins[:-1], mcdf).reshape(image.shape)

        return equalized_image.astype(np.uint8)

    def HYBRID_HE(self):
        image = self.image
        clip_limit = 2.0
        tile_size = (8, 8)
        alpha = 0.2
        beta = 0.3
        # Step 1: Apply adaptive histogram equalization (AHE)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        ahe = clahe.apply(image)

        # Step 2: Apply contrast limited adaptive histogram equalization (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        cl = clahe.apply(image)

        # Step 3: Apply brightness preserving dynamic histogram equalization (BPDHE)
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf / cdf.max()
        equalized = cv2.equalizeHist(image)
        equalized_alpha = cv2.addWeighted(image, alpha, equalized, 1 - alpha, beta)

        # Step 4: Merge the results
        merged = cv2.addWeighted(ahe, 0.3, cl, 0.5, 0)
        merged = cv2.addWeighted(merged, 0.7, equalized_alpha, 0.3, 0)

        return merged

    # Multi - scale Histogram Equalization(MSHE)
    def MSHE(self):
        img = self.image
        scales = [0.5, 1.0, 1.5]
        # Convert the input image to float
        img = img.astype(np.float32)

        # Apply histogram equalization at each scale
        img_eq = np.zeros_like(img)
        for scale in scales:
            # Resize the image to the current scale
            resized_img = cv2.resize(img, None, fx=scale, fy=scale)

            # Equalize the histogram of the resized image
            hist_eq = cv2.equalizeHist(resized_img.astype(np.uint8))

            # Resize the equalized image back to the original size
            resized_eq = cv2.resize(hist_eq, img.shape[::-1])

            # Accumulate the equalized images at different scales
            img_eq += resized_eq

        # Normalize the accumulated image
        img_eq /= len(scales)

        # Convert the image back to uint8
        img_eq = img_eq.astype(np.uint8)

        return img_eq

    # Histogram Equalization
    def GHE(self):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        histogram = Histogram()
        LUT = histogram.histogram_equalization(image_1d)
        return utils.LUT_image(LUT)


    # Brightness-preserving Bi-Histogram Equalization (BBHE)
    def BBHE(self):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        mean = np.mean(image_1d)
        mean = math.floor(mean)
        histogram = Histogram()
        LUT = histogram.histogram_equalization_threshold(image_1d, mean)
        return utils.LUT_image(LUT)


    # Recursive Mean-Separate Histogram Equalization (RMSHE)
    def RMSHE(self, recursive=2):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        histogram = Histogram()
        LUT = histogram.histogram_equalization_recursively(image_1d, np.mean, recursive)
        return utils.LUT_image(LUT)


    # Minimum Mean Brightness Error Histogram Equalization (MMBEBHE)
    def MMBEBHE(self):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        mbe = utils.minimum_mean_brightness_error(image_1d)
        histogram = Histogram()
        LUT = histogram.histogram_equalization_threshold(image_1d, mbe)
        return utils.LUT_image(LUT)


    # Dualistic Sub-Image Histogram Equalization (DSIHE)
    def DSIHE(self):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        median = np.median(image_1d)
        median = math.floor(median)
        histogram = Histogram()
        LUT = histogram.histogram_equalization_threshold(image_1d, median)
        return utils.LUT_image(LUT)

    # Dynamic Contrast Ratio Gamma Correction (DCRGC)
    def DCRGC(self, contrast_intensity, gamma):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        gamma_reverse = [0.0] * 256
        for i in range(1, 256):
            gamma_reverse[i] = (i / 255) ** gamma

        normalized_foundation_histogram = np.array([0.0] * 256)
        for i in range(1, 256):
            normalized_foundation_histogram[i] = gamma_reverse[i] - gamma_reverse[i - 1]

        histogram, _ = np.histogram(image_1d, 256, [0, 255])
        histogram = histogram / len(image_1d)

        normalized_combination_histogram = histogram * contrast_intensity + normalized_foundation_histogram * (
                1 - contrast_intensity)
        normalized_combination_cdf = normalized_combination_histogram.cumsum()

        LUT = normalized_combination_cdf * 255
        LUT = LUT.astype('uint8')

        return utils.LUT_image(LUT)


    # Adaptive Gamma Correction with Weighting Distribution (AGCWD)
    def AGCWD(self, alpha=0.5):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()
        length = len(image_1d)

        pdf, _ = np.histogram(image_1d, 256, [0, 255])
        pdf = pdf / length
        highest_probabilitiy = pdf.max()
        lowest_probability = pdf.min()

        weight_distribution = highest_probabilitiy * (
                (pdf - lowest_probability) / (highest_probabilitiy - lowest_probability)) ** alpha
        weight_distribution_sum = np.sum(weight_distribution)

        weight_distribution_scale = weight_distribution / weight_distribution_sum

        LUT = np.array([0.0] * 256)
        for i in range(0, 256):
            LUT[i] = 255 * (i / 255) ** (1 - weight_distribution_scale[i])
        LUT = LUT.astype('uint8')

        return utils.LUT_image(LUT)


    # Adaptive Gamma Correction Image Enhancement (AGCIE)
    def AGCIE(self, contrast_threshold=3):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten() / 255

        mean = np.mean(image_1d)
        std = np.std(image_1d)
        LUT = np.arange(0, 256) / 255

        if std <= 1 / (4 * contrast_threshold):
            gamma = -math.log(std, 2)
        else:
            gamma = math.exp((1 - (mean + std)) / 2)

        if mean >= 0.5:
            LUT = 255 * (LUT ** gamma)
        else:
            for i in range(0, 256):
                LUT[i] = 255 * (LUT[i] ** gamma / (LUT[i] ** gamma + (1 - LUT[i] ** gamma) * mean ** gamma))

        LUT = LUT.astype('uint8')

        return utils.LUT_image(LUT)

    # Adaptive Gamma Correction Color Preserving Framework (AGCCPF)
    def AGCCPF(self, alpha=0.5):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        pdf, _ = np.histogram(image_1d, 256, [0, 255])

        image_equalization = self.GHE()
        image_equalization_1d = image_equalization.flatten()

        pdf_equalization, _ = np.histogram(image_equalization_1d, 256, [0, 255])

        smooth_pdf = 0.5 * pdf + 0.5 * pdf_equalization
        smooth_pdf_scale = smooth_pdf / np.sum(smooth_pdf)

        cdf = smooth_pdf_scale.cumsum()

        LUT = np.array([0.0] * 256)
        for i in range(0, 256):
            LUT[i] = 255 * (i / 255) ** (1 - cdf[i])
        LUT = LUT.astype('uint8')

        return utils.LUT_image(LUT)

    # Range Limited Bi-Histogram Equalization (RLBHE)
    def RLBHE(self):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        otsu_threshold, _ = cv.threshold(image_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        otsu_threshold = math.floor(otsu_threshold)

        pdf, _ = np.histogram(image_1d, 256, [0, 255])
        image_mean = 0
        lower_cumulative = 0
        for i in range(0, 256):
            image_mean += i * pdf[i]

            if i <= otsu_threshold:
                lower_cumulative += pdf[i]

        length = len(image_1d)
        image_mean /= length
        lower_cumulative /= length

        a = lower_cumulative
        b = 2 * image_mean - otsu_threshold - (1 - a)
        x_0 = 0
        x_l = 255
        for i in range(0, 500):
            temp = 2 * (a * x_0 + (1 - a) * x_l - b)
            x_0 -= temp * a
            x_l -= temp * (1 - a)

        if x_0 < 0:
            x_0 = 0
        elif x_0 > otsu_threshold:
            x_0 = otsu_threshold
        else:
            x_0 = math.floor(x_0)

        if x_l > 255:
            x_l = 255
        elif x_l <= otsu_threshold:
            x_l = otsu_threshold + 1
        else:
            x_l = math.floor(x_l)

        histogram = Histogram()
        LUT = histogram.histogram_equalization_threshold(image_1d, otsu_threshold, x_0, x_l)
        return utils.LUT_image(LUT)

    # Recursive Sub-Image Histogram Equalization (RSIHE)
    def RSIHE(self, recursive=2):
        utils = Utils(self.image, self.color_space)
        image_gray = utils.image_gray()
        image_1d = image_gray.flatten()

        histogram = Histogram()
        LUT = histogram.histogram_equalization_recursively(image_1d, np.median, recursive)
        return utils.LUT_image(LUT)
