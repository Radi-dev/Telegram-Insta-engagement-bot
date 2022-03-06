from email import message
from telegram import Update, Bot, Chat, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Filters, InlineQueryHandler, Dispatcher
from config import TOKEN
import logging
import requests
import random
import time
from handlers.messages import echo
from queue import Queue
from threading import Thread
from handlers.panel import handle_admin
from handlers.callbacks import callback_answer, send_ad
from.functions import Subscriber


updater = Updater(token=TOKEN, use_context=True, workers=32)
dispatcher = updater.dispatcher
bot = Bot(token=TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

subscriber = Subscriber()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_to_message_id=update.message.message_id)


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    msg = "cancelled"
    update.message.reply_text(msg)
    return ConversationHandler.END


def send_adv(update: Update, context: CallbackContext):
    send_ad(update.message)
    return ConversationHandler.END


def subscriber_activate(update: Update, context: CallbackContext):
    subscriber.activate(update.message)
    return ConversationHandler.END


def subscriber_activate_premium(update: Update, context: CallbackContext):
    subscriber.activate(update.message, premium=True)
    return ConversationHandler.END


def subscriber_deactivate(update: Update, context: CallbackContext):
    subscriber.deactivate(update.message)
    return ConversationHandler.END


def subscriber_deactivate_premium(update: Update, context: CallbackContext):
    subscriber.deactivate(update.message, premium=True)
    return ConversationHandler.END


def calbcks(update: Update, context: CallbackContext):
    # context.bot.send_message(
    #    chat_id=update.effective_chat.id, text=update.callback_query.data)
    return callback_answer(update.callback_query)


conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(calbcks, run_async=True)],
    states={"ad": [MessageHandler(Filters.text, send_adv)], "activate": [
        MessageHandler(Filters.text, subscriber_activate)], "deactivate": [
        MessageHandler(Filters.text, subscriber_deactivate)], "activate_premium": [
        MessageHandler(Filters.text, subscriber_activate_premium)], "deactivate_premium": [
        MessageHandler(Filters.text, subscriber_deactivate_premium)], },
    fallbacks=[CommandHandler('cancel', cancel)])


def admin(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        handle_admin(update.message)
   # context.bot.send_message(
   #     chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_to_message_id=update.message.message_id)


# def echo(update: Update, context: CallbackContext):
#    if update.message.chat.type != "private":
#        update.message.reply_text(update.message.text.encode('utf-8').decode())
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


def onjoin(update: Update, context: CallbackContext):
    context.bot.delete_message(
        chat_id=update.message.chat_id, message_id=update.message.message_id)


join_handler = MessageHandler(Filters.status_update, onjoin)
start_handler = CommandHandler('start', start, run_async=True)
#calbcks_handler = CallbackQueryHandler(calbcks, run_async=True)
admin_handler = CommandHandler('admin', admin, run_async=True)
echo_handler = MessageHandler(Filters.text & (
    ~Filters.command), echo, run_async=True)
inline_caps_handler = InlineQueryHandler(inline_caps, run_async=True)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)
# dispatcher.add_handler(calbcks_handler)
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(join_handler)
