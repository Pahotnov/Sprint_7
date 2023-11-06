import string
import random

import allure


@allure.title("Генерация случайных логина, пароля и имени.")
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.title('Вернуть случайный логин')
def random_login():
    login = generate_random_string(10)
    return login
