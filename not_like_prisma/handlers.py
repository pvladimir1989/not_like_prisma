from telegram import ReplyKeyboardMarkup
import cv2
from not_like_prisma.keyboard import main_keyboard, greeting_text, filter_keyboard
from telegram.ext import Filters
from not_like_prisma.utils import make_folders, save_user_image, filter_user_image

# INPUT_PATH = None
# OUTPUT_PATH = None


def greet_user(update, context):
    print('Вызван /start')
    greet_keyboard = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    update.message.reply_text(greeting_text, reply_markup=greet_keyboard)


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def get_image(update, context):
    # global INPUT_PATH
    # global OUTPUT_PATH
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)  # получаем фотографию от пользователя
    input_path, output_path = save_user_image(user_photo)
    context.user_data["input"] = input_path
    context.user_data["output"] = output_path
    print(input_path, output_path)
    keyboard = ReplyKeyboardMarkup(filter_keyboard, resize_keyboard=True, row_width=2)
    update.message.reply_text('Фото получено', reply_markup=keyboard)


def send_filtered_photo(update, context):
    filters_dict = {'gray_filter': 'Серый', 'threshold_filter': 'Сегментирование',
                    'increase_brightness': 'Увеличение яркости',
                    'blur_filter': 'Размытие', 'sobel_filter': 'Фильтр Собеля', 'sepia': 'Сепия',
                    'cartoon': 'Мультфильм',
                    'pencil_scatch': 'Карандаш', 'pointillism': 'Пуантилизм'}
    chat_id = update.message.chat_id
    print(chat_id)  # check
    filter_attribute = update.message.text
    print(filter_attribute)  # check
    for keys, values in filters_dict.items():
        if filter_attribute == values:
            filter_attribute = keys
    # global INPUT_PATH
    # global OUTPUT_PATH
    input_path = context.user_data.get('input')
    output_path = context.user_data.get('output')
    image = input_path
    print(input_path)  # check
    print(output_path)  # check
    image = cv2.imread(input_path)
    edited_photo = filter_user_image(image, filter_attribute)
    cv2.imwrite(output_path, edited_photo)
    user_photo = open(output_path, 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=user_photo)
    user_photo.close()


def start_image(update, context):
    update.message.reply_text("Загрузите фотографию для обработки")
