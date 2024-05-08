from selenium import webdriver
from bs4 import BeautifulSoup
import csv

# Создание экземпляра драйвера Selenium (Chrome)
driver = webdriver.Chrome()

# URL сайта с ежедневной базой данных валют Центрального Банка России
url = "https://cbr.ru/currency_base/daily/"

# Переход на страницу сайта
driver.get(url)

# Получение содержимого страницы
html_content = driver.page_source

# Закрытие драйвера
driver.quit()

# Создание объекта BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, "html.parser")

# Нахождение таблицы с курсами валют
table = soup.find("table", {"class": "data"})

# Создание CSV файла для записи данных
with open("currency_rates.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Запись заголовков столбцов в CSV файл
    writer.writerow(["Date", "Currency", "Code", "Nominal", "Value"])

    # Извлечение данных из таблицы и запись в CSV файл
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        date = columns[0].text.strip()
        currency = columns[1].text.strip()
        code = columns[2].text.strip()
        nominal = columns[3].text.strip()
        value = columns[4].text.strip()
        writer.writerow([date, currency, code, nominal, value])

print("Данные успешно извлечены и записаны в файл currency_rates.csv")
