import pytest
import requests
import allure
from urls import Endpoints
from data import OrderTestData

@allure.epic("Управление заказами")
@allure.feature("Создание заказа и получение списка")
class TestCreateAndGetOrders:

    @allure.title("Параметризованный тест создания заказа с разным выбором цветов самоката")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, colors):
        payload = OrderTestData.BASE_ORDER_PAYLOAD.copy()
        payload["color"] = colors
        
        response = requests.post(Endpoints.ORDERS, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)

    @allure.title("Успешное получение общего списка заказов")
    def test_get_orders_list_success(self):
        response = requests.get(Endpoints.ORDERS)
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        assert len(response.json()["orders"]) > 0
