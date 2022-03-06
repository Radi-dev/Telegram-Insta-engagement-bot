import time
from config import bot


delete_list = []


def add_to_delete_que(chat_id, msg_id, max_time=10, start_time=time.time()):
    delete_schedule = {'max_time': max_time, 'start_time': start_time,
                       'chat': chat_id, 'message': msg_id}
    delete_list.append(delete_schedule)


def delete():
    new_list = []
    if len(delete_list) > 0:
        for i in delete_list:
            if time.time() - i["start_time"] >= i['max_time']:
                try:
                    bot.delete_message(i["chat"], i["message"])
                    delete_list.append(i)
                except:
                    pass
        for i in new_list:
            delete_list.remove(i)
