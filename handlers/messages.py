from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler


update1 = Update


def echo(update: update1, context: CallbackContext):
    """
    Checking The User's Message Within The Licensed Group
    """
    message_format = "Dx15 @instatravel.lifestyle https://www.instagram.com/p/CCk4PN9sz4S/"

    if update.message.chat.type == "group" or update.message.chat.type == "supergroup":

        # Check the message format
        text = update.message.text.encode('utf-8').decode()

        message = text.split(" ")

        if len(message[0]) < 1:
            print("no text")
            return
        if not message[0].upper() == "Dx15".upper():
            print("not Dx text")
            return

        if len(message) != 3:
            update.message.reply_text(f"""
                        Wrong Format! The right format is
                        {message_format}
                                        """, disable_web_page_preview=True)

        elif len(message[2].strip("/").split("/")) == 5:

            link = message[2]
            username = message[1].strip("@")

            #action = Action(username, link)
            try:
                # ----test async
                # for i in range(10000):
                #    print("doing action")
                #    print(i**i)
                # ----end test async

                # action.get_user_id()
                #post = action.get_media_id()
                post = None  # nein
            except:
                post = None
                print('didn\'t get posts')

            if post is None:
                update.message.reply_text(
                    f"This post was not found in the timeline feed of {username}", disable_web_page_preview=True
                )
