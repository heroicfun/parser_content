import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bots import db


def search(m, dicts):
    return [value for key, value in dicts.items() if m in key]


def driver_init():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options


def parse():
    chrome_options = driver_init()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    helper = {
        'habr': {
            'site_link': 'https://habr.com/ru/flows/develop/',
            'xpath_link': '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[1]/article/div[1]/h2/a',
            'xpath_name': '/html/body/div[1]/div[1]/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[1]/article/div[1]/h2/a/span'
        },
        'medium': {
            'site_link': 'https://medium.com',
            'xpath_link': '/html/body/div/div/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/a',
            'xpath_name': '/html/body/div/div/div[4]/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/a/h2'
        }
    }

    parsed_links = []
    parsed_names = []

    for site in helper.keys():
        driver.get(helper[site]['site_link'])
        time.sleep(3)
        links = driver.find_elements(By.XPATH, helper[site]['xpath_link'])
        names = driver.find_elements(By.XPATH, helper[site]['xpath_name'])
        for link, name in zip(links, names):
            parsed_links.append(link.get_attribute('href'))
            parsed_names.append(name.text.lower())

    dictionary = dict(zip(parsed_names, parsed_links))
    return dictionary


def form_query_results(result, shelf):
    response = []

    for part in result.split(" "):
        response.extend(search(part, shelf))

    return response


def post_processing(result):
    results = parse()
    shelf = db.open_db('database')
    db.write_to_db(results, shelf)
    response = form_query_results(result, shelf)
    db.close(shelf)
    return set(response)
