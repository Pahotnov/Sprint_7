import allure

from helpers import generate_random_string, random_login

import requests
import pytest

from urls import Urls


class TestCreateUser:

    @allure.title("Корректное создание нового пользователя")
    @allure.description("Проверка того, что курьера можно создать;"
                        " запрос возвращает правильный код ответа;"
                        " успешный запрос возвращает {\"ok\":true}")
    def test_create_new_user_correct_status_and_answer(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(Urls.CREATE_USER_URL, data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title("Создание второго одинакового пользователя")
    @allure.description("Проверка того, что нельзя создать двух одинаковых курьеров;"
                        " если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_create_new_user_twice(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        requests.post(Urls.CREATE_USER_URL, data=payload)
        response = requests.post(Urls.CREATE_USER_URL, data=payload)
        assert response.status_code == 409 and response.text == '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}'

    @allure.title("Создание пользователя без одного из обязательных полей")
    @allure.description("Проверка того, что нельзя создать нового курьера без обязательных полей;"
                        " если одного из полей нет, запрос возвращает ошибку")
    @pytest.mark.parametrize('login, password', [[random_login(), ''], ['', 'password12345']])
    def test_create_new_user_without_obligatory_fields(self, login, password):
        payload = {
            "login": login,
            "password": password,
            "firstName": "TestName"
        }

        response = requests.post(Urls.CREATE_USER_URL, data=payload)
        assert response.status_code == 400 and response.text == '{"code":400,"message":"Недостаточно данных для создания учетной записи"}'
