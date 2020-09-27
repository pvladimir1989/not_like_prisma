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


if __name__ == "__main__":
    gray_filter(
'input/AgACAgIAAxkBAAIBl19w3r9Q5hAZ6qWR6gvMCdAs9AR_AAK7rzEbigABiEtz2aE2zLy4KN4M5JcuAAMBAAMCAAN5AAMCFwEAARsE.jpg',
'output/AgACAgIAAxkBAAIBl19w3r9Q5hAZ6qWR6gvMCdAs9AR_AAK7rzEbigABiEtz2aE2zLy4KN4M5JcuAAMBAAMCAAN5AAMCFwEAARsE.jpg',
'AgACAgIAAxkBAAIBl19w3r9Q5hAZ6qWR6gvMCdAs9AR_AAK7rzEbigABiEtz2aE2zLy4KN4M5JcuAAMBAAMCAAN5AAMCFwEAARsE.jpg'
    )

