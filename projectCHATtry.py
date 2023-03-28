import requests
from bs4 import BeautifulSoup
import json

# url страницы, которую мы хотим спарсить
url = "https://magnit.katalog-ceny.ru/index.php?route=product/category&path=118_146"

# отправляем GET-запрос на получение HTML-кода страницы
response = requests.get(url)

# парсим HTML-код с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# создаем пустой список, в который будем добавлять словари для каждого продукта
products = []

# находим все div-контейнеры с информацией о продуктах на первой странице

for product in soup.find_all('div', class_='product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12'):
    name = product.find('div', class_='product-name').text.strip()
    price = product.find('p', class_='price').text.strip()

    # проверяем наличие старой цены
    old_price_element = product.find('span', class_='price-old')
    if old_price_element is not None:
        old_price = old_price_element.text.strip()
    else:
        old_price = ""

    # добавляем словарь с информацией о продукте в список
    products.append({
        "name": name,
        "price": price,
        "old_price": old_price
    })

# сохраняем список продуктов в файле json
with open("products.json", "w", encoding="utf-8") as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

print("Данные сохранены в файле products.json")