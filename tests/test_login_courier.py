import pytest
import requests
import allure
from urls import Endpoints
from data import ErrorMessages

@allure.epic("Управление курьерами")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера возвращает id")
    def test_courier_login_success(self, create_and_delete_courier):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"]}
        
        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка авторизации при отсутствии поля login или password")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field, create_and_delete_courier):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"]}
        del payload[missing_field]

        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)

         # Теперь бэкенд должен возвращать 400 на любое пропущенное обязательное поле
        assert response.status_code == 400
        
    @allure.title("Ошибка авторизации с неверными учетными данными")
    @pytest.mark.parametrize("wrong_data", [
        {"login": "non_existent_user_login", "password": "correct_password"},
        {"login": "correct_login", "password": "wrong_password_1234"}
    ])
    def test_login_with_incorrect_credentials(self, wrong_data, create_and_delete_courier):
        courier = create_and_delete_courier
        if wrong_data["login"] == "correct_login":
            payload = {"login": courier["login"], "password": wrong_data["password"]}
        else:
            payload = {"login": wrong_data["login"], "password": courier["password"]}
            
        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)
        
        assert response.status_code == 404
        assert ErrorMessages.LOGIN_NOT_FOUND in response.json().get("message")
