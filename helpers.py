import string
import random

import allure


@allure.title("Генерация рандомных логина, пароля и имени.")
def random_login():
    @allure.step("Генерирование рандомной строки в нижнем регистре.")
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    return login
