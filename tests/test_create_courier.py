import pytest
import requests
import allure
from urls import Endpoints
from data import ErrorMessages

@allure.epic("Управление курьерами")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_create_courier_success(self, generate_courier_data):
        payload = generate_courier_data()
        
        # Выполняем только целевое действие теста
        response = requests.post(Endpoints.CREATE_COURIER, json=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        # Логику удаления переносим из finally прямо сюда, но без if
        login_res = requests.post(Endpoints.LOGIN_COURIER, json={"login": payload["login"], "password": payload["password"]})
        login_res.raise_for_status()
        
        courier_id = login_res.json()["id"]
        requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")

     @allure.title("Нельзя создать двух абсолютно одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, create_and_delete_courier):
        duplicate_payload = create_and_delete_courier
        response = requests.post(Endpoints.CREATE_COURIER, json=duplicate_payload)
        
        assert response.status_code == 409
        assert ErrorMessages.REGISTRATION_DUPLICATE in response.json().get("message")

    @allure.title("Нельзя создать курьера с уже занятым логином")
    def test_cannot_create_courier_with_existing_login(self, create_and_delete_courier, generate_courier_data):
        existing_courier = create_and_delete_courier
        new_payload = generate_courier_data()
        new_payload["login"] = existing_courier["login"]
        
        response = requests.post(Endpoints.CREATE_COURIER, json=new_payload)
        
        assert response.status_code == 409
        assert ErrorMessages.REGISTRATION_DUPLICATE in response.json().get("message")

    @allure.title("Ошибка создания курьера при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_cannot_create_courier_without_required_field(self, missing_field, generate_courier_data):
        payload = generate_courier_data()
        del payload[missing_field]
        
        response = requests.post(Endpoints.CREATE_COURIER, json=payload)
        
        assert response.status_code == 400
        assert ErrorMessages.REGISTRATION_MISSING_FIELDS in response.json().get("message")
