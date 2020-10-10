import os
from filters import ImageFilters

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



