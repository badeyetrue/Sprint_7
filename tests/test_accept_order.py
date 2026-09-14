import requests
import allure
from urls import Endpoints
from data import ErrorMessages, OrderTestData

@allure.epic("Управление заказами")
@allure.feature("Принять заказ")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self, create_and_delete_courier):
        courier = create_and_delete_courier
        login_res = requests.post(Endpoints.LOGIN_COURIER, json={"login": courier["login"], "password": courier["password"]})
        courier_id = login_res.json()["id"]
        
        order_res = requests.post(Endpoints.ORDERS, json=OrderTestData.BASE_ORDER_PAYLOAD)
        track = order_res.json()["track"]
        
        get_order_res = requests.get(Endpoints.GET_ORDER_BY_NUMBER, params={"t": track})
        order_id = get_order_res.json()["order"]["id"]
        
        response = requests.put(f"{Endpoints.ACCEPT_ORDER}{order_id}", params={"courierId": courier_id})
        
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка, если не передан id курьера")
    def test_accept_order_missing_courier_id(self):
        order_id = 12345
        response = requests.put(f"{Endpoints.ACCEPT_ORDER}{order_id}")
        
        assert response.status_code == 400
        assert ErrorMessages.ORDER_MISSING_DATA in response.json().get("message")

    @allure.title("Ошибка, если передан неверный id курьера")
    def test_accept_order_invalid_courier_id(self):
        order_id = 12345
        response = requests.put(f"{Endpoints.ACCEPT_ORDER}{order_id}", params={"courierId": 999999})
        
        assert response.status_code == 404
        assert ErrorMessages.COURIER_NOT_FOUND_ACCEPT in response.json().get("message")

    @allure.title("Ошибка, если не передан id заказа")
    def test_accept_order_missing_order_id(self):
        response = requests.put(Endpoints.ACCEPT_ORDER, params={"courierId": 1111})
        assert response.status_code in [400, 404, 405]

    @allure.title("Ошибка, если передан неверный id заказа")
    def test_accept_order_invalid_order_id(self, create_and_delete_courier):
        courier = create_and_delete_courier
        login_res = requests.post(Endpoints.LOGIN_COURIER, json={"login": courier["login"], "password": courier["password"]})
        courier_id = login_res.json()["id"]
        
        response = requests.put(f"{Endpoints.ACCEPT_ORDER}999999", params={"courierId": courier_id})
        
        assert response.status_code == 404
        assert ErrorMessages.ORDER_NOT_FOUND_ACCEPT in response.json().get("message")
