import time

import telebot, pyshorteners
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

bot = telebot.TeleBot('5208795479:AAG9a9sa3hsU8_L2PNn5h1WsznjhmTBl9Mc')

from selenium.webdriver.chrome.options import Options
import shelve


def search(m, dicts):
    return [value for key, value in dicts.items() if m in key]


@bot.message_handler(commands=['start'])
def send_start_msg(m):
    bot.send_message(m.chat.id, "hello, enter a search query")


shorter = pyshorteners.Shortener()


@bot.message_handler(content_types=['text'])
def send_user_message(m):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get('https://habr.com/ru/flows/develop/')

    links = []
    medium = [[], []]
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
    driver.get('https://medium.com')
    time.sleep(5)
    for i in range(30):
        try:
            elem = driver.find_element_by_xpath(
                f'/html/body/div/div/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/div[{i + 1}]/div/div/div/a')
            medium[0].append(elem.get_attribute('href'))
        except:
            continue

    for i in range(1, len(medium[0]) + 1):
        elem = driver.find_element_by_xpath(
            f'/html/body/div/div/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/div[{i}]/div/div/div/a/h2').text
        medium[1].append(elem.lower())

    shelf = shelve.open('database')

    dictionary = dict(zip(names, links))

    medium_dict = dict(zip(medium[1], medium[0]))
    for key, value in dictionary.items():
        if key not in shelf.keys():
            shelf[key] = value
    for key, value in medium_dict.items():
        if key not in shelf.keys():
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
        if 'tinyurl' not in item:
            bot.send_message(m.chat.id, shorter.tinyurl.short(item))
        else:
            bot.send_message(m.chat.id, item)
    shelf.close()


bot.polling(none_stop=True, interval=0)

