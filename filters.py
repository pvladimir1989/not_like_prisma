from glob import glob
import os 

import cv2

def gray_filter(input_image_path, output_image_path, file_name):
    try:
        image = cv2.imread(input_image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_image_path, gray_image)
    except Exception:
        print('something wrong')
    cv2.imwrite(output_image_path, gray_image)

