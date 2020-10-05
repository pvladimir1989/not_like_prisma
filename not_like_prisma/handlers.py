from glob import glob
import os 

from telegram import ReplyKeyboardMarkup
import cv2
from filters import gray_filter
from keyboard import keyboard
from utils import make_folders


def greet_user(update, context):
    print('Вызван /start')
    greet_keyboard = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Вызван /start', reply_markup = greet_keyboard)

def talk_to_me(update, context):
    text = update.message.text
    print (text)
    update.message.reply_text(text)


def save_user_image(user_photo):
    make_folders()
    input_image_path = os.path.join('input', f'{user_photo.file_id}.jpg')
    output_image_path = os.path.join('output', f'{user_photo.file_id}.jpg')  
    user_photo.download(input_image_path)
    return input_image_path, output_image_path

def filter_user_image(input_image_path):
    edited_photo = gray_filter(input_image_path)
    return edited_photo

def processing_user_photo(update, context):
    chat_id = update.message.chat_id
    user_photo = context.bot.getFile(update.message.photo[-1].file_id) # получаем фотографию от пользователя 
    input_image_path, output_image_path = save_user_image(user_photo) # сохраняем фото и прописываем пути 
    update.message.reply_text('принял фото')
    # блок для обработки фото 
    update.message.reply_text('обрабатываю фото')
    image = cv2.imread(input_image_path)
    edited_photo = filter_user_image(image)
    cv2.imwrite(output_image_path, edited_photo)
    # отправка фото
    update.message.reply_text('отправляю фото')
    context.bot.send_photo(chat_id = chat_id, photo = open(output_image_path, 'rb'))
    photo.close()

