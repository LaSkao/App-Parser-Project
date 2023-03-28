import requests
from bs4 import BeautifulSoup
import json
from time import sleep

# url страницы, которую мы хотим спарсить
url = "https://magnit.katalog-ceny.ru/index.php?route=product/category&path=118_143&page="

# создаем пустой список, в который будем добавлять словари для каждого продукта
products = []

# обходим все страницы с продуктами
page_num = 1
while True:
    response = requests.get(url + str(page_num))

    # проверяем, что получен ответ со статусом 200 OK
    if response.status_code != 200:
        break

    # парсим HTML-код с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # находим все div-контейнеры с информацией о продуктах на текущей странице
    for product in soup.find_all('div', class_='product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12'):
        name = product.find('div', class_='product-name').text.strip()
        price = product.find('p', class_='price').text.strip()

        # проверяем наличие старой цены
        old_price_element = product.find('span', class_='price-old')
        if old_price_element is not None:
            old_price = old_price_element.text.strip()
        else:
            old_price = " "

        # добавляем словарь с информацией о продукте в список
        products.append({
            "name": name,
            "price": price,
            "old_price": old_price
        })

        # выводим информацию о продукте в консоль
        print(name)
        print(price)
        print(old_price)
        print()

        # задержка перед парсингом следующего продукта
        sleep(0.1)

    page_num += 1

file_path = "C:/Users/laskao/products.json"

# сохраняем список продуктов в файле json
try:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

    print("Данные сохранены в файле products.json")
except Exception as e:
    print("Произошла ошибка при записи в файл:", e)