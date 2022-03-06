from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ParseMode
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from main.functions import Action
from config import bot
import emoji
import time
from config import ADMIN_USERNAME
from .deleter import add_to_delete_que


a = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":scroll: Dx15 List", use_aliases=True), callback_data="list")
keyboard = telegram.InlineKeyboardMarkup([[a]])


def echo(update: Update, context: CallbackContext):
    """
    Checking The User's Message Within The Licensed Group
    """
    message_format = "Dx15 @instatravel.lifestyle https://www.instagram.com/p/CCk4PN9sz4S/"
    wrong_format_message = f""" 
@{update.message.from_user.first_name} : 
Wrong Format! The right format is
{message_format}
                """

    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":

        # Check the message format
        text = update.message.text.encode('utf-8').decode()

        message = text.split(" ")

        if len(message[0]) < 1:
            return
        if not message[0].upper() == "Dx15".upper():
            return

        if len(message) != 3:
            update.message.reply_text(
                wrong_format_message, disable_web_page_preview=True)

        elif len(message[2].strip("/").split("/")) == 5:

            link = message[2]
            username = message[1].strip("@")

            action = Action(username, link)
            try:
                # ----test async
                # for i in range(10000):
                #    print("doing action")
                #    print(i**i)
                # ----end test async

                action.get_user_id()
                post = action.get_media_id()
            except:
                post = None

            if post is None:
                update.message.reply_text(
                    f"This post was not found in the timeline feed of {username}", disable_web_page_preview=True
                )
            else:

                # CHECK IF USER HAS PERFORMED LIKE ACTIONS
                action.check_likes()
                action.check_comments()

                status = action.get_status()
                if action.check_if_exists_in_list():
                    update.message.reply_text(
                        emoji.emojize(
                            f"@{update.message.from_user.first_name} :This post has already been approved", use_aliases=True))
                else:

                    if status != True:
                        update.message.reply_text(
                            emoji.emojize(f":x: {status}", use_aliases=True)
                        )
                    else:
                        action.remove_user()
                        update.message.reply_text(
                            emoji.emojize(
                                f"@{update.message.from_user.first_name} :heavy_check_mark: Approved", use_aliases=True)
                        )
                        action.add_to_list()

        else:
            update.message.reply_text(
                wrong_format_message,
                disable_web_page_preview=True
            )

    elif update.message.chat.type == "private":

        message = f"""
<b>:bangbang: STOP Liking & Commenting :bangbang:</b>

:raising_hand: Join the Premium Subscribers and post without engaging back or get auto comments every time you post to our pods :raising_hand:

:point_right: Contact admin:
@{ADMIN_USERNAME}
"""

        reply = update.message.reply_text(
            emoji.emojize(message, use_aliases=True),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )

        #
#        reply = bot.send_message(
#            msg.chat.id,
#            f"""
# Welcome Back {msg.from_user.username},
#
#    <b>Dx15 Group Administrative Panel.</b>""",
#            reply_markup=keyboard,
#            parse_mode=telegram.ParseMode.HTML
#        )

    else:
        pass

    try:
        #start_time = time.time()
        bot.delete_message(update.message.chat.id, update.message.message_id)

        add_to_delete_que(update.message.chat.id,
                          reply.message_id, max_time=30)
    except:
        pass
