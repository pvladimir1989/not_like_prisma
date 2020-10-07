import cv2
from pandas import np


def gray_filter(image):
    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception:
        print('something wrong')
    return gray_image


def threshold_filter(image):
    try:
        _, th1 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO_INV)
    except Exception:

        print('something wrong')
    return th1


def increase_brightness(image, value=300):
    try:

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    except Exception:
        print('something wrong')
    return img


def blur_filter(image):
    try:
        blur_image = cv2.blur(image, (9, 9), 0)
    except Exception:
        print('something wrong')
    return blur_image


def sobel_filter(image):
    try:
        laplacian_image = cv2.Laplacian(image, cv2.CV_8U)
    except Exception:
        print('something wrong')
    return laplacian_image


def sepia(image):
    try:
        img = image
        # original = img.copy()
        img = np.array(img, dtype=np.float64)  # converting to float to prevent loss
        img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                            [0.349, 0.686, 0.168],
                                            [0.393, 0.769, 0.189]]))  # multipying image with special sepia matrix
        img[np.where(img > 255)] = 255  # normalizing values greater than 255 to 255
        img = np.array(img, dtype=np.uint8)  # converting back to int

    except Exception:
        print('something wrong')
    return img


def cartoon(image):
    try:
        img = image
        edges1 = cv2.bitwise_not(cv2.Canny(img, 100, 200))  # for thin edges and inverting the mask obatined
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)  # applying median blur with kernel size of 5
        edges2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)  # thick edges
        dst = cv2.edgePreservingFilter(img, flags=2, sigma_s=64,
                                       sigma_r=0.25)  # you can also use bilateral filter but that is slow
        # flag = 1 for RECURS_FILTER (Recursive Filtering) and 2 for  NORMCONV_FILTER (Normalized Convolution). NORMCONV_FILTER produces sharpening of the edges but is slower.
        # sigma_s controls the size of the neighborhood. Range 1 - 200
        # sigma_r controls the how dissimilar colors within the neighborhood will be averaged. A larger sigma_r results in large regions of constant color. Range 0 - 1
        cartoon1 = cv2.bitwise_and(dst, dst, mask=edges1)  # adding thin edges to smoothened image
        cartoon2 = cv2.bitwise_and(dst, dst, mask=edges2)  # adding thick edges to smoothened image

    except Exception:
        print('something wrong')
    return cartoon2


def pencil_scatch(image):
    try:
        img = image
        dst_gray, dst_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07,
                                               shade_factor=0.05)  # inbuilt function to generate pencil sketch in both color and grayscale
        # sigma_s controls the size of the neighborhood. Range 1 - 200
        # sigma_r controls the how dissimilar colors within the neighborhood will be averaged. A larger sigma_r results in large regions of constant color. Range 0 - 1
        # shade_factor is a simple scaling of the output image intensity. The higher the value, the brighter is the result. Range 0 - 0.1
    except Exception:
        print('something wrong')
    return dst_color
