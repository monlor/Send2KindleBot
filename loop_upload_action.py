import telebot
import time
import subprocess
import sys
from config_loader import load_config

config = load_config()
TOKEN = config["DEFAULT"]["TOKEN"]

bot = telebot.TeleBot(TOKEN)

for x in range(0,50):
    try:
        bot.send_chat_action(sys.argv[1], "upload_document")
        time.sleep(5)
    except:
        pass
