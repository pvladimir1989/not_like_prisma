from glob import glob
import os

from telegram import ReplyKeyboardMarkup
import cv2
from filters import ImageFilters
from keyboard import main_keyboard, greeting_text, filter_keyboard
from telegram.ext import Filters
from utils import make_folders, save_user_image, filter_user_image

INPUT_PATH = None
OUTPUT_PATH = None


def greet_user(update, context):
    print('Вызван /start')
    greet_keyboard = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    update.message.reply_text(greeting_text, reply_markup=greet_keyboard)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def get_image(update, context):
    global INPUT_PATH
    global OUTPUT_PATH
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)  # получаем фотографию от пользователя
    INPUT_PATH, OUTPUT_PATH = save_user_image(user_photo)
    keyboard = ReplyKeyboardMarkup(filter_keyboard, resize_keyboard=True)
    update.message.reply_text('Фото получено', reply_markup=keyboard)


def send_filtered_photo(update, context):
    chat_id = update.message.chat_id
    filter_attribute = update.message.text
    global INPUT_PATH
    global OUTPUT_PATH
    image = INPUT_PATH
    image = cv2.imread(INPUT_PATH)
    edited_photo = filter_user_image(image, filter_attribute)
    cv2.imwrite(OUTPUT_PATH, edited_photo)
    user_photo = open(OUTPUT_PATH, 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=user_photo)
    user_photo.close()


def start_image(update, context):
    update.message.reply_text("Загрузите фотографию для обработки")
