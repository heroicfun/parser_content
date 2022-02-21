import pyshorteners
import telebot
from dotenv import load_dotenv
import os

from bots import parser


shorter = pyshorteners.Shortener()
load_dotenv()

bot = telebot.TeleBot(str(os.getenv('token')))


@bot.message_handler(commands=['start'])
def send_start_msg(m):
    bot.send_message(m.chat.id, "hello, enter a search query")


@bot.message_handler(content_types=['text'])
def send_user_message(m):
    result = m.text
    final_set = parser.post_processing(result)
    for item in final_set:
        if 'tinyurl' not in item:
            bot.send_message(m.chat.id, shorter.tinyurl.short(item))
        else:
            bot.send_message(m.chat.id, item)


bot.polling(none_stop=True, interval=0)
