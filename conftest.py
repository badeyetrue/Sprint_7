import pytest
import requests
from urls import Endpoints
from helpers import get_random_courier_data  # Импортируем чистый хелпер

@pytest.fixture
def courier_manager():
    """Фикстура-менеджер для гибкого отслеживания курьеров в тестах.
    Позволяет зарегистрировать любого курьера на удаление.
    """
    couriers_to_delete = []

    def _register_for_deletion(payload):
        couriers_to_delete.append(payload)
        return payload

    yield _register_for_deletion  # Передаем функцию-регистратор в тест

    # Шаг очистки (Teardown) для всех зарегистрированных курьеров
    for courier_payload in couriers_to_delete:
        login_payload = {
            "login": courier_payload["login"], 
            "password": courier_payload["password"]
        }
        
        try:
            login_response = requests.post(Endpoints.LOGIN_COURIER, json=login_payload)
            login_response.raise_for_status() 
            
            courier_id = login_response.json()["id"]
            
            delete_response = requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")
            delete_response.raise_for_status()
        except Exception as e:
            print(f"\n[Teardown Warning] Не удалось удалить курьера: {e}")


@pytest.fixture
def create_and_delete_courier(courier_manager):
    """Фикстура для позитивных тестов: автоматически создает курьера 
    и регистрирует его в менеджере для последующего удаления.
    """
    courier_payload = get_random_courier_data()
    
    # Регистрация курьера в системе
    requests.post(Endpoints.CREATE_COURIER, json=courier_payload)
    
    # Регистрируем в менеджере очистки
    courier_manager(courier_payload)
    
    yield courier_payload  # Передаем данные в тест
