import requests
from urls import Endpoints
from helpers import get_random_courier_data  # Импортируем хелпер для негативных кейсов

def test_success_create_courier(create_and_delete_courier):
    """Позитивный тест: курьера можно создать (проверяем повторный запрос или логику)"""
    courier_payload = create_and_delete_courier
    
    # Фикстура уже создала курьера, мы можем проверить, например, повторное создание
    response = requests.post(Endpoints.CREATE_COURIER, json=courier_payload)
    
    assert response.status_code == 409  # Пример: база должна ответить, что логин занят
    assert response.json().get("message") == "Этот логин уже занят"


def test_create_courier_without_login(courier_manager):
    """Негативный тест: создание курьера без логина"""
    # 1. Генерируем данные без логина через хелпер
    payload = get_random_courier_data(login="")
    
    # 2. Регистрируем в менеджере (на случай, если бэкенд ошибочно создаст курьера)
    courier_manager(payload)
    
    # 3. Делаем проверочный запрос
    response = requests.post(Endpoints.CREATE_COURIER, json=payload)
    
    assert response.status_code == 400
    assert response.json().get("message") == "Недостаточно данных для создания учетной записи"


def test_create_duplicate_courier(courier_manager):
    """Негативный тест: создание двух одинаковых курьеров"""
    payload = get_random_courier_data()
    
    # Регистрируем данные в очистку и создаем первого курьера
    courier_manager(payload)
    requests.post(Endpoints.CREATE_COURIER, json=payload)
    
    # Пытаемся создать точно такого же курьера второй раз
    response = requests.post(Endpoints.CREATE_COURIER, json=payload)
    
    assert response.status_code == 409
    assert response.json().get("message") == "Этот логин уже занят"
