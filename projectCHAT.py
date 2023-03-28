import requests
import json
from bs4 import BeautifulSoup

# url страницы, которую мы хотим спарсить
url = "https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol"

# отправляем GET-запрос на получение HTML-кода страницы
response = requests.get(url)

# парсим HTML-код с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# находим все div-контейнеры с информацией о продуктах на первой странице
products = soup.find_all('div', class_='catalog-2-level-product-card product-card subcategory-or-type__products-item catalog--online offline-prices-sorting--all with-prices-drop')

# для каждого продукта получаем название и цену
result = []
for product in products:
    name = product.find('span', class_='product-card-name__text').text.strip()
    price = product.find('span', class_='product-price__sum-rubles').text.strip()
    result.append({"name": name, "price": price})

# проверяем, есть ли на странице ссылка на следующую страницу
# проверяем, есть ли на странице ссылка на следующую страницу
nextpage = soup.find('a', class_='v-pagination__navigation catalog-paginate__item')
while nextpage is not None:
    # Получаем ссылку на следующую страницу и повторяем все те же шаги
    url = nextpage['href']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findall('div', class_='product-info')
    for product in products:
        name = product.find('h2').text.strip()
        price = product.find('div', class_='price').text.strip()
        result.append({"name": name, "price": price})

    # Ищем ссылку на следующую страницу на текущей странице
    nextpage = soup.find('a', class_='v-pagination__navigation catalog-paginate__item')

# сохраняем полученные данные в JSON-файл
with open('products.json', 'w') as f:
    json.dump(result, f)