import requests
import allure
from urls import Endpoints
from data import ErrorMessages, OrderTestData

@allure.epic("Управление заказами")
@allure.feature("Получить заказ по его номеру")
class TestGetOrderByNumber:

    @allure.title("Успешное получение информации о заказе по трек-номеру")
    def test_get_order_by_track_number_success(self):
        order_res = requests.post(Endpoints.ORDERS, json=OrderTestData.BASE_ORDER_PAYLOAD)
        track_number = order_res.json()["track"]
        
        response = requests.get(Endpoints.GET_ORDER_BY_NUMBER, params={"t": track_number})
        
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track_number

    @allure.title("Ошибка при запросе без номера трека")
    def test_get_order_without_track_number(self):
        response = requests.get(Endpoints.GET_ORDER_BY_NUMBER)
        
        assert response.status_code == 400
        assert ErrorMessages.ORDER_MISSING_DATA in response.json().get("message")

    @allure.title("Ошибка при поиске по несуществующему трек-номеру")
    def test_get_order_by_non_existent_track(self):
        response = requests.get(Endpoints.GET_ORDER_BY_NUMBER, params={"t": 99999999})
        
        assert response.status_code == 404
        assert ErrorMessages.ORDER_NOT_FOUND_TRACK in response.json().get("message")
