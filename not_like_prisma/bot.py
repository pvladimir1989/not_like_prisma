import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from not_like_prisma.handlers import greet_user, talk_to_me, start_image, get_image, send_filtered_photo
import not_like_prisma.settings as settings

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


def main():
    my_bot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Начнем обработку фотографии)$'), start_image))
    dp.add_handler(MessageHandler(Filters.photo, get_image))
    dp.add_handler(MessageHandler(Filters.regex('^(Серый)$|^(Сегментирование)$|^(Увеличение яркости)$|^(Размытие)$|^('
                                                'Фильтр Собеля)$|^(Сепия)$|^(Мультфильм)$|^(Карандаш)$|^(Пуантилизм)$'),
                                  send_filtered_photo))
    # dp.add_handler(MessageHandler(Filters.text, send_filtered_photo))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    my_bot.start_polling()


if __name__ == "__main__":
    main()
