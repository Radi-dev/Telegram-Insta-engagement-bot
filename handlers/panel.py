from config import ADMIN_ID, telegram, bot
import emoji


a = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Activate Subscriber", use_aliases=True), callback_data="activate")
b = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Deactivate Subscriber", use_aliases=True), callback_data="deactivate")
c = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":scroll: Send Advertisement", use_aliases=True), callback_data="ad")
keyboard = telegram.InlineKeyboardMarkup([[a, b], [c]])

# @bot.message_handler(commands=['admin', 'panel'])


def handle_admin(msg):
    """Admin feature to the bot management"""
    if msg.from_user.id == int(ADMIN_ID):
        bot.send_message(
            msg.chat.id,
            f"""
Welcome Back {msg.from_user.username},
            
    <b>Dx15 Group Administrative Panel.</b>""",
            reply_markup=keyboard,
            parse_mode=telegram.ParseMode.HTML
        )

    else:
        bot.send_message(
            msg.chat.id,
            "You are not authorized to use this command", reply_to_message_id=msg.message_id
        )
