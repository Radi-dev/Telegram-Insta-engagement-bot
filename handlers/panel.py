from config import ADMIN_ID, telegram, bot
import emoji


a = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Activate Subscriber", use_aliases=True), callback_data="activate")
b = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Deactivate Subscriber", use_aliases=True), callback_data="deactivate")
c = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Activate Premium Subscriber", use_aliases=True), callback_data="activate_premium")
d = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":memo: Deactivate Premium Subscriber", use_aliases=True), callback_data="deactivate_premium")
e = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":loudspeaker: Send Advertisement", use_aliases=True), callback_data="ad")
# f = telegram.InlineKeyboardButton(text=emoji.emojize(
#    ":scroll: Send Advertisement", use_aliases=True), callback_data="ad")
g = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":boy: Subscribers List", use_aliases=True), callback_data="subs")
h = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":princess: Premium List", use_aliases=True), callback_data="subs_premium")
i = telegram.InlineKeyboardButton(text=emoji.emojize(
    ":clipboard: Dx15 List", use_aliases=True), callback_data="list")
keyboard = telegram.InlineKeyboardMarkup([[a, b], [c, d], [e], [g, h], [i]])


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
