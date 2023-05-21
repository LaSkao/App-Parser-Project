import requests
from bs4 import BeautifulSoup
import json

DEBUG = 0
DEBUG_SLEEP_TIME = 0.5
if DEBUG: from time import sleep 

# url страницы, которую мы хотим спарсить
url = "https://magnit.katalog-ceny.ru/tovary/?page="
# файл для дампа инфы
file_path = "magnit.json"

# обходим все страницы с продуктами
page_num = 1
products = []

while True:
    response = requests.get(url + str(page_num))
    # проверяем, что получен ответ со статусом 200 OK
    if response.status_code != 200: 
        print("Проблемы с подключением")
        break

    # парсим HTML-код с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    print("-"*10+f"PAGE {page_num}"+"-"*10)

    # находим все div-контейнеры с информацией о продуктах на текущей странице
    parsed_products = soup.find_all('div', class_='product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12')
    if len(parsed_products) == 0: break
    for product in parsed_products:
        name = product.find('div', class_='product-name').text.strip()

        # Проверяем наличие классов price_new и old_price
        if product.find('span', class_='price-new') is not None and product.find('span', class_='price-old') is not None:
            price_new = product.find('span', class_='price-new').text.strip()
            old_price = product.find('span', class_='price-old').text.strip()
        else:
            # Если классов price_new и old_price нет, сохраняем только цену
            price = product.find('p', class_='price').text.strip()
            price_new = price
            old_price = price

        # добавляем словарь с информацией о продукте в список
        products.append({
            "name": name,
            "discounted_price": price_new,
            "price": old_price,
            "store": 'magnit'
        })
        if DEBUG: print(products[-1], end='\n\n')
    
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(products, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Произошла ошибка при записи в файл:", e)
    page_num += 1
    if DEBUG: sleep(DEBUG_SLEEP_TIME)
