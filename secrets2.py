import os

auth_token = os.getenv('TOKEN')
# Значением переменной auth_token будет 123

account_sid = os.getenv('ACCOUNT_SID')
# А эту переменную мы не определили в пространстве переменных окружения
# Значением переменной account_sid будет None
