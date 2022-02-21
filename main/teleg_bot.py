from email import message
from telegram import Update, Bot, Chat, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from config import TOKEN
import logging
import requests
import random
import time
from handlers.messages import echo


updater = Updater(token=TOKEN, use_context=True, workers=32)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_to_message=update)


# def echo(update: Update, context: CallbackContext):
#    if update.message.chat.type != "private":
#        update.message.reply_text(update.message.text)
#    postt = requests.get("https://jsonplaceholder.typicode.com/posts/").json()
#    postte = postt[random.randrange(0, 99)]["body"]
#    context.bot.send_message(
#        chat_id=update.effective_chat.id, text=postte)


def inline_caps(update: Update, context: CallbackContext):
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
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(inline_caps_handler)
