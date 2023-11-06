import allure
import pytest
import requests

from helpers import generate_random_string
from urls import Urls


@allure.title("Создание нового курьера и возврат списка его данных")
@allure.description("Метод регистрации нового курьера возвращает список из логина и пароля;"
                    " если регистрация не удалась, возвращает пустой список")
@pytest.fixture
def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Urls.CREATE_USER_URL, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass
