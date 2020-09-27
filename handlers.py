from glob import glob
import os 

from filters import gray_filter

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Вызван /start')

def talk_to_me(update, context):
    text = update.message.text
    print (text)
    update.message.reply_text(text)

def send_image(update, context):
    image_list = glob('images/*.jp*g')
    pass

def get_user_image(update, context):
    """
    функция принимает фотографию из чата с ботом и сохраняет ее в папку download
    Далее применяется фильтр, который переводит фото в ч/б (градации серого) и сохраняет ее в папку images 
    """
    chat_id = update.message.chat_id # получаем чат айди пользователя

    update.message.reply_text('Принимаю фото')
    os.makedirs('input', exist_ok = True) #добавляется папка input
    os.makedirs('output', exist_ok = True) #добавляется папка output
    
    user_photo = context.bot.getFile(update.message.photo[-1].file_id) # получаем фотографию от пользователя 
    
    input_image_path = os.path.join('input', f'{user_photo.file_id}.jpg') 
    output_image_path = os.path.join('output', f'{user_photo.file_id}.jpg') 
    
    user_photo.download(input_image_path)
    update.message.reply_text('Фото сохранено')
    
    # вызываем функцию обработки изображения
    gray_filter(input_image_path= f'{input_image_path}', output_image_path = f'{output_image_path}', file_name=f'{user_photo.file_id}.jpg')
    update.message.reply_text('Фото изменено')
    context.bot.send_photo(chat_id = chat_id, photo = open(f'{output_image_path}', 'rb'))
    
    