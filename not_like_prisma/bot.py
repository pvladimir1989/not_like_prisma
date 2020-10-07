# стандартные библиотеки
import logging

# side библиотеки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# локальные модули
from handlers import (greet_user, talk_to_me, processing_user_photo)

from telegram import replykeyboardmarkup

import settings as settings

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
    # dp.add_handler(MessageHandler(Filters.photo, processing_user_photo))

    dp.add_handler(CommandHandler("cat", processing_user_photo))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), processing_user_photo))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
