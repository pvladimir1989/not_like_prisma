import os

import cv2
from pandas import np

from not_like_prisma.filters import ImageFilters


def make_folders():
    os.makedirs('input', exist_ok=True)  # добавляется папка input
    os.makedirs('output', exist_ok=True)  # добавляется папка output


def save_user_image(user_photo):
    make_folders()
    input_image_path = os.path.join('input', f'{user_photo.file_id}.jpg')
    output_image_path = os.path.join('output', f'{user_photo.file_id}.jpg')
    user_photo.download(input_image_path)
    return input_image_path, output_image_path


def filter_user_image(image, filter_attribute):
    filter = ImageFilters(image)
    edited_photo = getattr(filter, filter_attribute)
    return edited_photo()


# from kernel
def limit_size(img, max_x, max_y=0):
    if max_x == 0:
        return img

    if max_y == 0:
        max_y = max_x

    ratio = min(1.0, float(max_x) / img.shape[1], float(max_y) / img.shape[0])

    if ratio != 1.0:
        shape = (int(img.shape[1] * ratio), int(img.shape[0] * ratio))
        return cv2.resize(img, shape, interpolation=cv2.INTER_AREA)
    else:
        return img


def clipped_addition(img, x, _max=255, _min=0):
    if x > 0:
        mask = img > (_max - x)
        img += x
        np.putmask(img, mask, _max)
    if x < 0:
        mask = img < (_min - x)
        img += x
        np.putmask(img, mask, _min)


def regulate(img, hue=0, saturation=0, luminosity=0):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    if hue < 0:
        hue = 255 + hue
    hsv[:, :, 0] += hue
    clipped_addition(hsv[:, :, 1], saturation)
    clipped_addition(hsv[:, :, 2], luminosity)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)
