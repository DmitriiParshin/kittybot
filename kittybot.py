import logging
import os
import requests

from dotenv import load_dotenv

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater


load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'


def get_new_image_cat():
    try:
        response = requests.get(CAT_URL)
    except Exception as error:
        print(error)
        response = requests.get(DOG_URL)

    response = response.json()
    return response[0].get('url')


def get_new_image_dog():
    try:
        response = requests.get(DOG_URL)
    except Exception as error:
        print(error)
        response = requests.get(CAT_URL)

    response = response.json()
    return response[0].get('url')


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image_cat())


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image_dog())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    reply_markup = ReplyKeyboardMarkup(
        [['/cats', '/dogs']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Тебе больше нравятся котики или пёсики? Жми '
             f'"/cats" - если котики, "/dogs" - если пёсики',
        reply_markup=reply_markup
    )

def main():
    updater = Updater(token=TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cats', new_cat))
    updater.dispatcher.add_handler(CommandHandler('dogs', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
