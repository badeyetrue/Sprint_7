import pytest
import requests
from faker import Faker
from urls import Endpoints

fake = Faker()

@pytest.fixture
def generate_courier_data():
    """Фабрика для создания данных курьера с предсказуемой структурой"""
    def _generate(login=None, password=None, first_name=None):
        return {
            "login": login or fake.user_name(),
            "password": password or fake.password(length=10),
            "firstName": first_name or fake.first_name()
        }
    return _generate

@pytest.fixture
def courier_manager():
    """Универсальный менеджер курьеров: управляет очисткой без использования if."""
    couriers_to_delete = []

    def _register_for_deletion(payload):
        couriers_to_delete.append(payload)
        return payload

    yield _register_for_deletion  # Передаем функцию-регистратор в тесты

    # Шаг очистки (Teardown) для всех зарегистрированных курьеров
    for courier_payload in couriers_to_delete:
        login_payload = {
            "login": courier_payload["login"], 
            "password": courier_payload["password"]
        }
        
        # Если курьер не создался в тесте, логин упадет, raise_for_status() вызовет ошибку.
        # Использование try/except здесь допустимо, так как это защищает teardown от прерывания,
        # если тестировался негативный кейс.
        try:
            login_response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
            login_response.raise_for_status() 
            
            courier_id = login_response.json()["id"]
            
            delete_response = requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")
            delete_response.raise_for_status()
        except Exception as e:
            # Позволяет pytest продолжить удаление остальных курьеров, если их несколько
            print(f"Не удалось удалить курьера: {e}")
