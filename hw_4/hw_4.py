from lxml import html           # Импортируем модуль для работы с HTML и XPath
import requests                 # Импортируем модуль для отправки HTTP-запросов
from pprint import pprint       # Импортируем функцию pprint для красивого вывода данных
from bs4 import BeautifulSoup as bs  # Импортируем BeautifulSoup для обработки HTML
import re                       # Импортируем модуль для работы с регулярными выражениями
import urllib                   # Импортируем urllib для работы с URL
from datetime import datetime, date, time  # Импортируем datetime для работы с датой и временем

# Заголовки для HTTP-запросов, чтобы притворяться браузером
header = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 '
                       'Mobile/15E148 Safari/604.1'}

# Список сайтов для сбора новостей
news_aggregators = {'https://news.mail.ru',
                   'https://m.lenta.ru/parts/news',
                   'https://yandex.ru/news/'}

result = []  # Список для хранения результата сбора новостей

# Функция для сбора новостей с указанного агрегатора
def get_news(aggregator):
        response = requests.get(aggregator, headers=header)  # Отправляем GET-запрос на сайт
        root = html.fromstring(response.text)  # Получаем DOM страницы с помощью lxml

        if aggregator == 'https://news.mail.ru':
            # Используем XPath для поиска элементов новостей на сайте
            items = root.xpath("//a[@class='item item_side_left entity']")
            for item in items:
                dict = {}  # Словарь для хранения данных о новости
                link = str(item.xpath(".//@href")[0])
                if re.search('card', str(link)) or re.search('r.mail.ru', str(link)):
                    print("Не новости или статьи где не указана дата и источник: " + str(link))
                else:
                    if not re.search(aggregator, link):
                        link = aggregator + link
                    try:
                        article_page = requests.get(link, headers=header)
                        article = html.fromstring(article_page.text)  # Получаем DOM страницы новости
                        article_param = article.xpath("//div[@class='article__params']")[0]
                        dict['link'] = link
                        dict['title'] = item.xpath(".//text()")
                        dict['date'] = str(article_param.xpath(".//@datetime")).replace("['", "").replace("+03:00']", "").replace("T", " ")
                        dict['source'] = article_param.xpath(".//@href")
                        result.append(dict)  # Добавляем данные о новости в список результатов
                    except Exception as e:
                        print(e)

        elif aggregator == 'https://m.lenta.ru/parts/news':
            items = root.xpath("//div[@class='parts-page__item']")  # Ищем блоки с новостями на сайте
            for item in items:
                try:
                    dict = {}   # Словарь для хранения данных о новости
                    # Используем XPath для поиска элементов новости в блоке
                    dict['link'] = aggregator.replace("parts/news","") + \
                                   str(item.xpath(".//@href")).replace("['/", "").replace("/']", "")
                    dict['title'] = item.xpath(".//div[@class='card-mini__title']/text()")
                    dict['source'] = aggregator
                    datime = str(datetime.now())[:11]
                    dict['date'] = datime + str(item.xpath(".//time[@class='card-mini__date']/text()")).replace("['", "").replace("']", "")
                    result.append(dict)  # Добавляем данные о новости в список результатов
                except Exception as e:
                    print(e)

        elif aggregator == 'https://yandex.ru/news/':
            items = root.xpath("//div[@class='card__body']")  # Ищем блоки с новостями на сайте
            for item in items:
                dict = {}  # Словарь для хранения данных о новости
                try:
                    # Используем XPath для поиска элементов новости в блоке
                    dict['link'] = item.xpath(
                        ".//a[@class='Link link card__link link-like link-like_type_turbo-navigation-react']/@href")
                    dict['title'] = item.xpath(
                        ".//a[@class='Link link card__link link-like link-like_type_turbo-navigation-react']/text()")
                    dict['source'] = item.xpath(".//@aria-label")[0]
                    datime = str(datetime.now())[:11]
                    dict['date'] = datime + str(item.xpath(".//span[@class ='sport-date card__source-date']/text()")).replace("['", "").replace("']", "")
                    result.append(dict)  # Добавляем данные о новости в список результатов
                except Exception as e:
                    print(e)

# Функция для сбора новостей со всех агрегаторов
def news():
    for aggregator in news_aggregators:
        get_news(aggregator)  # Вызываем функцию для сбора новостей с каждого агрегатора
    return result

pprint(news())  # Выводим результат сбор
