import allure
import requests
import pytest

from helpers import random_login


class TestLoginUser:

    # Курьер может авторизоваться, успешный запрос возвращает id
    @allure.title("Успешная авторизация пользователя")
    @allure.description("Курьер может авторизоваться, успешный запрос возвращает id")
    def test_success_user_login(self, register_new_courier_and_return_login_password):
        login_pass_name = register_new_courier_and_return_login_password
        payload = {
            "login": login_pass_name[0],
            "password": login_pass_name[1]
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 200 and "id" in response.text

    # Для авторизации нужно передать все обязательные поля;
    # система вернёт ошибку, если неправильно указать логин или пароль;
    # если какого-то поля нет, запрос возвращает ошибку;
    # если авторизоваться под несуществующим пользователем, запрос возвращает ошибку;
    @allure.title("Авторизация пользователя без одного из обязательных полей")
    @allure.description("Для авторизации нужно передать все обязательные поля;"
                        "система вернёт ошибку, если неправильно указать логин или пароль;"
                        "если какого-то поля нет, запрос возвращает ошибку;"
                        "если авторизоваться под несуществующим пользователем, запрос возвращает ошибку;")
    @pytest.mark.parametrize('login, password', [[random_login(), ''], ['', 'password12345']])
    def test_user_login_without_obligatory_fields(self, login, password):
        # собираем тело запроса
        payload = {
            "login": login,
            "password": password
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 400 and response.text == '{"code":400,"message":"Недостаточно данных для входа"}'

    @allure.title("Авторизация несуществующего пользователя")
    @allure.description("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_user_login_with_not_existing_data(self):
        # собираем тело запроса
        payload = {
            "login": "Test",
            "password": "Test"
        }
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 404 and response.text == '{"code":404,"message":"Учетная запись не найдена"}'
