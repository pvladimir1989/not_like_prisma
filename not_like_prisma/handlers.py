from glob import glob
import os

from telegram import ReplyKeyboardMarkup
import cv2
from filters import ImageFilters
from keyboard import main_keyboard, greeting_text, filter_keyboard
from telegram.ext import Filters
from utils import make_folders


def greet_user(update, context):
    print('Вызван /start')
    greet_keyboard = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    update.message.reply_text(greeting_text, reply_markup=greet_keyboard)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def save_user_image(user_photo):
    make_folders()
    input_image_path = os.path.join('input', f'{user_photo.file_id}.jpg')
    output_image_path = os.path.join('output', f'{user_photo.file_id}.jpg')
    user_photo.download(input_image_path)
    return input_image_path, output_image_path


def filter_user_image(input_image_path):
    edited_photo = ImageFilters.pencil_scatch(input_image_path)
    return edited_photo


# def filter_user_image(image, filter_atribute):
#     filter = Filters(image)
#     edited_photo = getattr(filter, filter_atribute)
#     return edited_photo()


def start_image(update, context):
    update.message.reply_text("Загрузите фотографию для обработки")


def get_image(update, context):
    global INPUT_PATH
    global OUTPUT_PATH
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)  # получаем фотографию от пользователя
    INPUT_PATH, OUTPUT_PATH = save_user_image(user_photo)
    keyboard = ReplyKeyboardMarkup(filter_keyboard, resize_keyboard=True)
    update.message.reply_text('Фото получено', reply_markup=keyboard)
    return 'user_photo'


def send_filtered_photo(update, context):
    chat_id = update.message.chat_id
    filter_atribute = update.message.text
    global INPUT_PATH
    global OUTPUT_PATH
    image = INPUT_PATH
    image = cv2.imread(INPUT_PATH)
    edited_photo = filter_user_image(image, filter_atribute)
    cv2.imwrite(OUTPUT_PATH, edited_photo)
    user_photo = open(OUTPUT_PATH, 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=user_photo)
    user_photo.close()
    return 'edited_photo'


def processing_user_photo(update, context):
    chat_id = update.message.chat_id
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)  # получаем фотографию от пользователя
    input_image_path, output_image_path = save_user_image(user_photo)  # сохраняем фото и прописываем пути
    update.message.reply_text('принял фото')
    # блок для обработки фото
    update.message.reply_text('обрабатываю фото')
    image = cv2.imread(input_image_path)
    edited_photo = filter_user_image(image)
    cv2.imwrite(output_image_path, edited_photo)
    # отправка фото
    update.message.reply_text('отправляю фото')
    context.bot.send_photo(chat_id=chat_id, photo=open(output_image_path, 'rb'))
    user_photo.close()
