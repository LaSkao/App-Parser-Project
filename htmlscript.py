from flask import Flask, render_template, request
import json

app = Flask(__name__)

# загрузка данных из файла products.json
with open('products.json', encoding='utf-8') as file:
    products = json.load(file)

# количество продуктов на странице
page_size = 30

# рендеринг страницы с товарами
@app.route('/')
def show_products():
    page_num = request.args.get('page', default=1, type=int)
    start = (page_num - 1) * page_size
    end = start + page_size
    products_on_page = products[start:end]

    # вычисляем количество страниц
    num_pages = (len(products) - 1) // page_size + 1

    # вычисляем список страниц для отображения
    if num_pages <= 10:
        pages_to_show = range(1, num_pages+1)
    else:
        if page_num <= 6:
            pages_to_show = range(1, 11)
        elif page_num >= num_pages - 5:
            pages_to_show = range(num_pages - 9, num_pages+1)
        else:
            pages_to_show = range(page_num - 5, page_num + 5)

    # формируем контекст для шаблона
    context = {
        'products': products_on_page,
        'page_num': page_num,
        'page_size': page_size,
        'total': len(products),
        'pages_to_show': pages_to_show, # добавляем переменную pages_to_show в контекст
        'num_pages': num_pages,
    }

    return render_template('index.html', **context)

# поиск товара по названию
@app.route('/search')
def search_products():
    query = request.args.get('q')

    # фильтруем список продуктов по запросу пользователя
    filtered_products = [product for product in products if query.lower() in product['name'].lower()]

    # формируем контекст для шаблона
    context = {
        'products': filtered_products,
        'query': query,
        'total': len(filtered_products),
    }

    return render_template('search.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
