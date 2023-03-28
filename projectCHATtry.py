import requests
from bs4 import BeautifulSoup

# url страницы, которую мы хотим спарсить
url = "https://magnit.katalog-ceny.ru/index.php?route=product/category&path=118_146"

# отправляем GET-запрос на получение HTML-кода страницы
response = requests.get(url)

# парсим HTML-код с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# находим все div-контейнеры с информацией о продуктах на первой странице
products = soup.find_all('div', class_='product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12')

# для каждого продукта получаем название, цену и скидку (если есть)
for product in products:
    name = product.find('div', class_='product-name').text.strip()
    price = product.find('p', class_='price').text.strip()
    discount = product.find('span', class_='price-old')
    if discount:
        discount = discount.text.strip()
        print("Название: {}\nЦена: {}\nСкидка: {}\n".format(name, price, discount))
    else:
        print("Название: {}\nЦена: {}\n".format(name, price))