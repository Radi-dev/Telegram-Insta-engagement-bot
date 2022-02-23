from email import message
from telegram import Update, Bot, Chat, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler, Dispatcher
from config import TOKEN
import logging
import requests
import random
import time
from handlers.messages import echo, update1
from queue import Queue
from threading import Thread
#from app import update1


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: update1, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_to_message_id=update.message.message_id)


# def echo(update: Update, context: CallbackContext):
#    if update.message.chat.type != "private":
#        update.message.reply_text(update.message.text.encode('utf-8').decode())
#    postt = requests.get("https://jsonplaceholder.typicode.com/posts/").json()
#    postte = postt[random.randrange(0, 99)]["body"]
#    context.bot.send_message(
#        chat_id=update.effective_chat.id, text=postte)


def inline_caps(update: update1, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


start_handler = CommandHandler('start', start, run_async=True)
echo_handler = MessageHandler(Filters.text & (
    ~Filters.command), echo, run_async=True)
inline_caps_handler = InlineQueryHandler(inline_caps, run_async=True)

update_queue = Queue()
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, update_queue)


def setup_for_Flask():

    ##### Register handlers here #####
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(inline_caps_handler)
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    return (update_queue, dispatcher)


# dispatch()
