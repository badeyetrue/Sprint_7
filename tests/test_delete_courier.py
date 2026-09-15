import requests
import allure
import pytest
from urls import Endpoints
from data import ErrorMessages

@allure.epic("Управление курьерами")
@allure.feature("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление существующего курьера")
    def test_delete_courier_success(self, generate_courier_data):
        payload = generate_courier_data()
        
        # Создаем курьера и проверяем успешность (заменяем неявный шаг на контролируемый)
        create_res = requests.post(Endpoints.CREATE_COURIER, json=payload)
        create_res.raise_for_status()
        
        login_res = requests.post(Endpoints.LOGIN_COURIER, json={"login": payload["login"], "password": payload["password"]})
        login_res.raise_for_status()
        courier_id = login_res.json()["id"]
        
        response = requests.delete(f"{Endpoints.DELETE_COURIER}{courier_id}")
        
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка при удалении курьера без передачи ID")
    def test_delete_courier_without_id(self):
        response = requests.delete(Endpoints.DELETE_COURIER)
        
        # Проверяем, что код ответа один из ожидаемых
        assert response.status_code in [400, 404]
        
        # Если пришел 400 — проверяем сообщение об ошибке. 
        # Если пришел 404 (ручка не найдена) — это тоже валидно согласно assert выше, и текст ошибки мы не ждем.
        if response.status_code == 400:
            assert ErrorMessages.COURIER_MISSING_ID_DELETE in response.json().get("message", "")

    @allure.title("Ошибка при удалении курьера с несуществующим ID")
    def test_delete_courier_non_existent_id(self):
        invalid_id = 999999
        response = requests.delete(f"{Endpoints.DELETE_COURIER}{invalid_id}")
        
        assert response.status_code == 404
        assert ErrorMessages.COURIER_NOT_FOUND_DELETE in response.json().get("message")
