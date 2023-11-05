import string
import random

import allure

from helpers import random_login

import requests
import pytest


class TestCreateUser:

    # Проверка того, что курьера можно создать;
    # запрос возвращает правильный код ответа;
    # успешный запрос возвращает {"ok":true}
    @allure.title("Корректное создание нового пользователя")
    @allure.description("Проверка того, что курьера можно создать;"
                        "запрос возвращает правильный код ответа;"
                        "успешный запрос возвращает {\"ok\":true}")
    def test_create_new_user_correct_status_and_answer(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    # Проверка того, что нельзя создать двух одинаковых курьеров;
    # если создать пользователя с логином, который уже есть, возвращается ошибка
    @allure.title("Создание второго одинакового пользователя")
    @allure.description("Проверка того, что нельзя создать двух одинаковых курьеров;"
                        "если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_create_new_user_twice(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 409 and response.text == '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}'

    # Проверка того, что нельзя создать нового курьера без обязательных полей;
    # если одного из полей нет, запрос возвращает ошибку
    @allure.title("Создание пользователя без одного из обязательных полей")
    @allure.description("Проверка того, что нельзя создать нового курьера без обязательных полей;"
                        "если одного из полей нет, запрос возвращает ошибку")
    @pytest.mark.parametrize('login, password', [[random_login(), ''], ['', 'password12345']])
    def test_create_new_user_without_obligatory_fields(self, login, password):
        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": "TestName"
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 400 and response.text == '{"code":400,"message":"Недостаточно данных для создания учетной записи"}'
