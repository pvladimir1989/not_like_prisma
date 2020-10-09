import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import (greet_user, talk_to_me, processing_user_photo, start_image,get_image,send_filtered_photo)

import settings

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
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Начнем обработку фотографии)$'), start_image))
    dp.add_handler(MessageHandler(Filters.photo, get_image))
    dp.add_handler(MessageHandler(Filters.photo, send_filtered_photo))
    # dp.add_handler(MessageHandler(Filters.photo, processing_user_photo))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
