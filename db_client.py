from pymongo import MongoClient

from secrets import db_user, db_password

# Подключение к локальному серверу MongoDB
client = MongoClient(f'mongodb://{db_user}:{db_password}@localhost:27017/')

# Выбор базы данных
db = client['mydatabase']

# Выбор коллекции
collection = db['mycollection']

document = {
    "user_id": "John Doe",
    "tz": 30,
    "files": "john.doe@example.com",
    "deadline": "10.10.2020"
}

result = collection.insert_one(document)
print(f"Inserted document ID: {result.inserted_id}")