import os

from dotenv import load_dotenv

load_dotenv()
# Теперь переменная TOKEN, описанная в файле .env,
# доступна в пространстве переменных окружения

token = os.getenv('TOKEN')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')