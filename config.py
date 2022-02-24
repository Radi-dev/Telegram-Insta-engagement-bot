from itertools import tee
import os
#from telebot import types
#import emoji

#from flask import Flask, request
from instagram_private_api import Client
from igramscraper.instagram import Instagram
from dotenv import load_dotenv
import telegram
load_dotenv()
#
DEBUG = True
#
# Telegram variables
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
#
# Instagram variables
USERNAME = os.getenv("USERNAMEE")
PASSWORD = os.getenv("PASSWORD")

client = Client(USERNAME, PASSWORD)

ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
GROUP_ID = os.getenv("GROUP_ID")

insta = Instagram()
#
#force_reply = types.ReplyKeyboardRemove(selective=False)
bot = telegram.Bot(token=TOKEN)
