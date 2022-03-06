from telegram import Bot
from telegram.ext import Dispatcher
from config import TOKEN
from queue import Queue
from threading import Thread
from .teleg_bot import start_handler, inline_caps_handler, echo_handler, admin_handler, calbck_handler

update_queue = Queue()
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, update_queue)


def setup_for_Flask():

    ##### Register handlers here #####
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(calbck_handler)
    dispatcher.add_handler(admin_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(inline_caps_handler)
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    return (update_queue, dispatcher)
