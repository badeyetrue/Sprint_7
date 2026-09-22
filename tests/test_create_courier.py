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
def create_and_delete_courier(generate_courier_data):
    """Фикстура: создает курьера перед тестом и гарантированно удаляет его после"""
    courier_payload = generate_courier_data()
    
    # Регистрация курьера
    requests.post(Endpoints.CREATE_COURIER, json=courier_payload)
    
    yield courier_payload  # Передаем данные в тест
    
    # Шаг очистки (Teardown): логин -> получение id -> удаление
    login_payload = {
        "login": courier_payload["login"], 
        "password": courier_payload["password"]
    }
    
    # Оборачиваем в try/except, чтобы возможные сбои при удалении курьера 
    # (например, если тест на удаление его уже стер) не аффектили статус теста.
    try:
        login_response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
        login_response.raise_for_status() 
        
        courier_id = login_response.json()["id"]
        
        delete_response = requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")
        delete_response.raise_for_status()
    except Exception as e:
        # Логируем ошибку в консоль, не прерывая выполнение pytest
        print(f"\n[Teardown Warning] Не удалось удалить курьера: {e}")
