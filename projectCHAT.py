import requests
import json
from bs4 import BeautifulSoup

# url страницы, которую мы хотим спарсить
url = "https://example.com/products"

# отправляем GET-запрос на получение HTML-кода страницы
response = requests.get(url)

# парсим HTML-код с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# находим все div-контейнеры с информацией о продуктах на первой странице
products = soup.findall('div', class='product-info')

# для каждого продукта получаем название и цену
result = []
for product in products:
    name = product.find('h2').text.strip()
    price = product.find('div', class_='price').text.strip()
    result.append({"name": name, "price": price})

# проверяем, есть ли на странице ссылка на следующую страницу
nextpage = soup.find('a', class='next-page')
while next_page:

    # получаем ссылку на следующую страницу и повторяем все те же шаги
    url = next_page['href']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findall('div', class='product-info')

    for product in products:
        name = product.find('h2').text.strip()
        price = product.find('div', class_='price').text.strip()
        result.append({"name": name, "price": price})

    # ищем ссылку на следующую страницу на текущей странице
    nextpage = soup.find('a', class='next-page')

# сохраняем полученные данные в JSON-файл
with open('products.json', 'w') as f:
    json.dump(result, f)
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList } from 'react-native';

export default function App() {

  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('path/to/products.json')
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((error) => console.error(error))
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.item}>
      <Text style={styles.title}>{item.name}</Text>
      <Text style={styles.subtitle}>{item.price}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={item => item.name}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  item: {
    backgroundColor: '#f9c2ff',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
    borderRadius: 10,
  },
  title: {
    fontSize: 24,
  },
  subtitle: {
    fontSize: 18,
    paddingTop: 10,
  },
});