import json

# Чтение данных из первого JSON-файла
with open('magnit.json', 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

# Чтение данных из второго JSON-файла
with open('5erka.json', 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# Объединение данных из двух списков в один
new_data = data1 + data2

# Запись объединенных данных в новый файл JSON
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
