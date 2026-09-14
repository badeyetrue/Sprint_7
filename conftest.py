import pytest
import requests
import random
import string
from urls import Endpoints

@pytest.fixture
def generate_courier_data():
    """Генератор случайных валидных данных курьера"""
    def _generate():
        length = 10
        letters = string.ascii_lowercase
        return {
            "login": ''.join(random.choice(letters) for _ in range(length)),
            "password": ''.join(random.choice(letters) for _ in range(length)),
            "firstName": ''.join(random.choice(letters) for _ in range(length))
        }
    return _generate

@pytest.fixture
def create_and_delete_courier(generate_courier_data):
    """Фикстура: создает курьера перед тестом и полностью удаляет его после"""
    courier_payload = generate_courier_data()
    
    # Регистрация курьера
    requests.post(Endpoints.CREATE_COURIER, json=courier_payload)
    
    yield courier_payload  # Передаем данные в тест
    
    # Шаг очистки (Teardown): авторизация -> получение id -> удаление
    login_payload = {"login": courier_payload["login"], "password": courier_payload["password"]}
    login_response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
    
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")

