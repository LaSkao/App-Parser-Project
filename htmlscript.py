from flask import Flask, render_template, request, session
import json 

app = Flask(__name__)

# загрузка данных из файла products.json
with open('products.json', encoding='utf-8') as file:
    products = json.load(file)

# количество продуктов на странице
page_size = 30

# установка секретного ключа для сессий
app.secret_key = 'mysecretkey'

# добавление товара в корзину
@app.route('/add_to_cart')
def add_to_cart():
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')

    # получаем корзину из сессии
    cart = session.get('cart', {})

    # добавляем товар в корзину
    cart[product_id] = cart.get(product_id, 0) + int(quantity)

    # сохраняем корзину в сессии
    session['cart'] = cart

    return 'Product added to cart successfully!'

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
        'pages_to_show': pages_to_show,
        'num_pages': num_pages,
    }

    return render_template('index.html', **context)

# поиск товара по названию
@app.route('/search')
def search_products():
    query = request.args.get('query_product')
    
    # фильтруем список продуктов по запросу пользователя
    if query:
        clear_query = query.lower().strip()
        filtered_products = [product for product in products
                                if clear_query in product.get('name', '').lower() 
                                    or clear_query in str(product.get('price_new', '')).lower()]
    else:
        filtered_products = []
    print(filtered_products)
    # формируем контекст для шаблона
    context = {
        'products': filtered_products,
        'query': query,
        'total': len(filtered_products),
    }

    return render_template('search.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
