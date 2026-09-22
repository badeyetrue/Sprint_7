import pytest
import requests
import allure
from urls import Endpoints
from data import ErrorMessages

@allure.epic("Управление курьерами")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера возвращает id")
    def test_courier_login_success(self, generate_courier_data, courier_manager):
        payload = generate_courier_data()
        
        # Сначала создаем курьера, чтобы было под кем логиниться
        requests.post(Endpoints.CREATE_COURIER, json=payload)
        courier_manager(payload) # Гарантируем очистку
        
        login_payload = {"login": payload["login"], "password": payload["password"]}
        response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка авторизации при отсутствии поля login или password")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field, generate_courier_data):
        # Для проверки отсутствия полей создавать реального курьера в БД не требуется
        payload = generate_courier_data()
        del payload[missing_field]

        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)

        assert response.status_code == 400
        assert ErrorMessages.LOGIN_MISSING_FIELDS in response.json().get("message", "")
        
    @allure.title("Ошибка авторизации: система возвращает ошибку, если неправильно указать логин")
    def test_login_with_incorrect_login(self):
        # Запрос с полностью выдуманными данными, курьера создавать не нужно
        payload = {"login": "completely_non_existent_login_123", "password": "any_password"}
        
        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)
        
        assert response.status_code == 404
        assert ErrorMessages.LOGIN_NOT_FOUND in response.json().get("message")

    @allure.title("Ошибка авторизации: система возвращает ошибку, если неправильно указать пароль")
    def test_login_with_incorrect_password(self, generate_courier_data, courier_manager):
        payload = generate_courier_data()
        
        # Создаем курьера в базе
        requests.post(Endpoints.CREATE_COURIER, json=payload)
        courier_manager(payload)
        
        # Логинимся с верным логином, но ломаем пароль
        login_payload = {"login": payload["login"], "password": "wrong_password_999"}
        
        response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
        
        assert response.status_code == 404
        assert ErrorMessages.LOGIN_NOT_FOUND in response.json().get("message")
