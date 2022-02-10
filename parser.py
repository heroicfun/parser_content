import telebot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import requests, json

bot = telebot.TeleBot('5208795479:AAG9a9sa3hsU8_L2PNn5h1WsznjhmTBl9Mc')

from selenium.webdriver.chrome.options import Options
import shelve

def search(m, dicts):
    return [value for key, value in dicts.items() if m in key]


@bot.message_handler(commands=['start'])
def send_start_msg(m):
    bot.send_message(m.chat.id, "hello, enter a search query")

@bot.message_handler(content_types=['text'])
def send_user_message(m):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get('https://habr.com/ru/flows/develop/')

    links = []

    for i in range(20):
        try:
            elem = driver.find_element_by_xpath(
                f'/html/body/div[1]/div[1]/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[1]/article[{i}]/div[1]/h2/a')
            links.append(elem.get_attribute('href'))
        except:
            continue

    names = []

    for i in range(1, len(links) + 1):
        elem = driver.find_element_by_xpath(
            f'/html/body/div[1]/div[1]/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[1]/article[{i}]/div[1]/h2/a/span').text

        names.append(elem.lower())
    shelf = shelve.open('database', 'n')

    dictionary = dict(zip(names, links))
    for key, value in dictionary.items():
        shelf[key] = value

    result = m.text

    parts = result.split(" ")
    final_set = []
    for part in parts:
        res = search(part, shelf)
        print(res)
        for item in res:
            if item not in final_set:
                final_set.append(item)
    for item in final_set:
        bot.send_message(m.chat.id, item)
    shelf.close()

bot.polling(none_stop=True, interval=0)
