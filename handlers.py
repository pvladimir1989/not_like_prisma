from glob import glob
import os 

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
    """
    update.message.reply_text('Принимаю фото')
    os.makedirs('download', exist_ok = True) #добавляется папка download
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('download', f'{user_photo.file_id}.jpg') 
    user_photo.download(file_name)
    update.message.reply_text('Фото сохранено')
