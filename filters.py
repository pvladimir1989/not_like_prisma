from glob import glob
import os 

import cv2

def gray_filter(image_path, file_name):
    image = cv2.imread(image_path)
    #os.chdir('./images') #необходимо поменять директорию, чтобы сохранить в images 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(file_name, gray_image) 

if __name__ == "__main__":
    image_path = glob('download/*.jp*g')[-1]
    file_name = 'AgACAgIAAxkBAAPhX3CB6m09u8QUIi8Erz1vfsgZ8iUAAiauMRuGaYBLg2apG4FsYU-SjaCWLgADAQADAgADeQADhe0BAAEbBA.jpg'
    gray_filter(image_path, file_name)



