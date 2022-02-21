import os
#import telebot
#import telegram
#from telebot import types
#import emoji
#import time
#import pickle
#from flask import Flask, request
#from instagram_private_api import Client
#from igramscraper.instagram import Instagram
from dotenv import load_dotenv
load_dotenv()
#
DEBUG = True
#
# Telegram variables
TOKEN = os.getenv("TOKEN")
#
# Instagram variables
#USERNAME = os.getenv("USERNAMEE")
#PASSWORD = os.getenv("PASSWORD")
#print(USERNAME, PASSWORD, TOKEN)
#
#WEBHOOK_URL = os.getenv("WEBHOOK_URL")
#
#bot = telebot.TeleBot(TOKEN, threaded=True)
#
#client = Client(USERNAME, PASSWORD)
#
#ADMIN_ID = os.getenv("ADMIN_ID")
#ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
#GROUP_ID = os.getenv("GROUP_ID")
#
#insta = Instagram()
#
#force_reply = types.ReplyKeyboardRemove(selective=False)
