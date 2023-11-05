import json

import allure
import requests
import pytest


class TestOrders:

    @allure.title("Создание заказа с разными цветами")
    @allure.description("Можно указать один из цветов — BLACK или GREY;"
                        "можно указать оба цвета;"
                        "можно совсем не указывать цвет;"
                        "тело ответа содержит track.")
    @pytest.mark.parametrize('color', ['BLACK', 'GREY', 'BLACK, GREY', ''])
    def test_create_order_with_different_colors(self, color):
        # собираем тело запроса
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": [
                color
            ]
        }

        payload = json.dumps(payload)
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload)
        assert response.status_code == 201 and 'track' in response.text

    @allure.title("Список заказов")
    @allure.description("Проверка, что в тело ответа возвращается непустой список заказов.")
    def test_get_list_of_orders(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
        response_in_json = response.json()
        assert response.status_code == 200 and "orders" in response.text and len(response_in_json['orders']) > 0
