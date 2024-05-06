import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['books']
collection = db['books_toscrape_com']

# Чтение файла JSON
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# # Вставка книг в коллекцию MongoDB
for item in data:
    collection.insert_one(item)

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]
print(first_doc)
# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# фильтрация документов по критериям
query = {'category': 'Travel'}
print(f"Количество документов c категорией 'Travel': {collection.count_documents(query)}")

# Использование проекции
query = {'category': 'Travel'}
projection = {"name": 1, "price": 1, "available": 1, "_id": 0}
proj_docs = collection.find(query, projection)
for doc in proj_docs:
    print(doc)

# Использование оператора $lt и $gte
AVAILABLE_1 = 2
AVAILABLE_2 = 20
query = {"available": {"$lt": AVAILABLE_1}}
print(f"Количество документов c категорией available < {AVAILABLE_1}: {collection.count_documents(query)}")
query = {"available": {"$gte": AVAILABLE_2}}
print(f"Количество документов c категорией available >= {AVAILABLE_2}: {collection.count_documents(query)}")

# Использование оператора $regex
WORD = "America"
query = {"name": {"$regex": WORD, "$options": "i"}}
print(f"Количество документов, содержащих '{WORD}': {collection.count_documents(query)}")

# Использование оператора $in
query = {"category": {"$in": ["Travel", "Romance", "Science Fiction"]}}
print(f"Количество документов в категории 'category': {collection.count_documents(query)}")

# Использование оператора $all
query = {"category": {"$all": ["Mystery"]}}
print(f"Количество документов в категории 'category': {collection.count_documents(query)}")

# Использование оператора $ne
query = {"category" : {"$ne": "Mystery"}}
print(f"Количество документов в категории 'category': {collection.count_documents(query)}")