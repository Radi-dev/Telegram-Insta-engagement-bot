from config import ADMIN_USERNAME, ADMIN_ID, GROUP_ID, bot, telegram
from main.functions import Subscriber
import json
from .deleter import add_to_delete_que
force_reply = telegram.ReplyKeyboardRemove(selective=False)


def callback_answer(call):
    """
    Button Response
    """
    if call.data == "list":

        # Fetch List
        file = open("main/list.json", 'r')
        data = json.loads(file.read())
        file.close()
        messg = ''.join([
            f"{i+1}) {data[i].get('media_url')} \n" for i in range(len(data))])
        try:
            reply = bot.send_message(
                call.message.chat.id,
                f"""
        <b>Dx15 INSTAGRAM LIST</b>

    1)  {data[0].get("media_url")}

    2)  {data[1].get("media_url")}

    3)  {data[2].get("media_url")}

    4)  {data[3].get("media_url")}

    5)  {data[4].get("media_url")}

    6)  {data[5].get("media_url")}

    7)  {data[6].get("media_url")}

    8)  {data[7].get("media_url")}

    9)  {data[8].get("media_url")}

    10)  {data[9].get("media_url")}

    11)  {data[10].get("media_url")}

    12)  {data[11].get("media_url")}

    13)  {data[12].get("media_url")}

    14)  {data[13].get("media_url")}

    15)  {data[14].get("media_url")}
        
                """,
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True
            )
        except IndexError:
            reply = bot.send_message(
                call.message.chat.id,
                f"<b>The Dx15 engagement list is almost complete! Contact @{ADMIN_USERNAME} to get registered to Global Trade Club community and grow your instagram presence</b>\n{messg}",
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True
            )

        # time.sleep(20)
        #bot.delete_message(call.message.chat.id, reply.message_id)
        add_to_delete_que(call.message.chat.id, reply.message_id, max_time=20)

    elif call.data == "ad":
        question = bot.send_message(
            call.from_user.id,
            "Paste your advestisement writing below to post to Dx15 Engagement Group....",
            reply_markup=force_reply
        )
        return "ad"

    elif call.data == "activate":

        question = bot.send_message(
            int(ADMIN_ID),
            "To add a new subscriber, paste the instagram username below",
            reply_markup=force_reply
        )
        return "activate"

    elif call.data == "deactivate":

        question = bot.send_message(
            int(ADMIN_ID),
            "To deactivate a subscriber, paste the instagram username below",
            reply_markup=force_reply
        )
        return "deactivate"
    elif call.data == "activate_premium":

        question = bot.send_message(
            int(ADMIN_ID),
            "To add a new subscriber, paste the instagram username below",
            reply_markup=force_reply
        )
        return "activate_premium"

    elif call.data == "deactivate_premium":
        question = bot.send_message(
            int(ADMIN_ID),
            "To deactivate_premium a subscriber, paste the instagram username below",
            reply_markup=force_reply
        )
        return "deactivate_premium"

    elif call.data == "subs":
        data = Subscriber().get_subscribers()
        messg = ''.join([f"{data.index(i)+1}) {i} \n" for i in data])
        bot.send_message(
            int(ADMIN_ID),
            f"""<b>List of All Currently Approved Subscribers</b>
{messg}
        """,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True
        )
    elif call.data == "subs_premium":
        data = Subscriber().get_subscribers(premium=True)
        messg = ''.join([f"{data.index(i)+1}) {i} \n" for i in data])
        bot.send_message(
            int(ADMIN_ID),
            f"""<b>List of All Premium Subscribers</b>
{messg}
        """,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        pass


def send_ad(msg):
    "Sends Add Message To Group"
    message = msg.text

    # Fetch List
    file = open("main/list.json", 'rb')
    data = json.loads(file.read())
    file.close()

    bot.send_message(
        int(GROUP_ID),
        f"""
<b>{message}</b>
        """,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True
    )
