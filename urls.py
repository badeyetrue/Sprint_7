BASE_URL = "https://qa-scooter.praktikum-services.ru/"

class Endpoints:
    # Ручки курьера
    CREATE_COURIER = f"{BASE_URL}api/v1/courier"
    LOGIN_COURIER = f"{BASE_URL}api/v1/courier/login"
    DELETE_COURIER = f"{BASE_URL}api/v1/courier/" # Нужен ID в конец пути

    # Ручки заказов
    ORDERS = f"{BASE_URL}api/v1/orders"
    ACCEPT_ORDER = f"{BASE_URL}api/v1/orders/accept/" # Нужен ID заказа в конец пути
    GET_ORDER_BY_NUMBER = f"{BASE_URL}api/v1/orders/track" # Номер передается через params ?t=
