import requests
from lxml import html
import csv

# URL веб-сайта с таблицей данных
url = 'https://cbr.ru/currency_base/daily/'

# Строка агента пользователя в заголовке HTTP-запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

try:
    # Отправляем GET-запрос на веб-сайт и получаем HTML-содержимое страницы
    response = requests.get(url, headers=headers)
    # Создаем объект ElementTree для парсинга HTML
    tree = html.fromstring(response.content)

    # Выражение XPath для выбора элементов таблицы
    rows = tree.xpath('//table[@class="data"]//tr')

    # Путь к CSV-файлу, в который будут сохранены данные
    csv_file = 'currency_rates.csv'

    # Открываем CSV-файл для записи
    with open(csv_file, 'w', newline='') as csvfile:
        # Создаем объект для записи в CSV-файл
        writer = csv.writer(csvfile)

        # Проходимся по строкам таблицы, начиная с второй строки (первая строка содержит заголовки столбцов)
        for row in rows[1:]:
            # Извлекаем данные из ячеек текущей строки
            data = [cell.text_content().strip() for cell in row.xpath('./td')]
            # Записываем данные в CSV-файл
            writer.writerow(data)

    print("Данные успешно сохранены в файл", csv_file)

except requests.exceptions.RequestException as e:
    print("Ошибка при выполнении запроса:", e)

except Exception as ex:
    print("Произошла ошибка:", ex)