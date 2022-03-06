from itertools import tee
import os
#from telebot import types
#import emoji

#from flask import Flask, request
from instagram_private_api import Client
from igramscraper.instagram import Instagram
from dotenv import load_dotenv
import telegram
import json
load_dotenv()
#
DEBUG = True
#
# Telegram variables
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
INITIAL_LIST = json.loads(os.getenv("INITIAL_LIST")) if os.getenv("INITIAL_LIST") else [
    {'media_id': '2484895178441043911', 'media_url': 'https://www.instagram.com/p/CJ8Hv_PDy_H/'}]
INITIAL_SUBS = json.loads(os.getenv("INITIAL_SUBS")) if os.getenv(
    "INITIAL_SUBS") else ['radi_dev', 'Hi']
#
# Instagram variables
USERNAME = os.getenv("USERNAMEE")
PASSWORD = os.getenv("PASSWORD")

#client = Client(USERNAME, PASSWORD)


insta = Instagram()
#
#force_reply = types.ReplyKeyboardRemove(selective=False)
bot = telegram.Bot(token=TOKEN)

ADMIN_ID = os.getenv("ADMIN_ID")
group_id = os.getenv("GROUP_ID")
GROUP_ID = group_id if group_id[0] == '-' else f'-{group_id}'

admin = bot.get_chat_member(GROUP_ID, ADMIN_ID)
ADMIN_USERNAME = admin.user.username
