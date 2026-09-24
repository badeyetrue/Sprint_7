class OrderTestData:
    BASE_ORDER_PAYLOAD = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 999 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-12-12",
        "comment": "Saske, come back to Konoha",
        "color": []
    }

class ErrorMessages:
    # Ошибки курьера
    REGISTRATION_DUPLICATE = "Этот логин уже используется. Попробуйте другой."
    REGISTRATION_MISSING_FIELDS = "Недостаточно данных для создания учетной записи"
    LOGIN_MISSING_FIELDS = "Недостаточно данных для входа"
    LOGIN_NOT_FOUND = "Учетная запись не найдена"
    COURIER_NOT_FOUND_DELETE = "Курьера с таким id нет"
    COURIER_MISSING_ID_DELETE = "Недостаточно данных"

    # Ошибки заказов
    ORDER_MISSING_DATA = "Недостаточно данных для поиска"
    COURIER_NOT_FOUND_ACCEPT = "Курьера с таким id не существует"
    ORDER_NOT_FOUND_ACCEPT = "Заказа с таким id не существует"
    ORDER_NOT_FOUND_TRACK = "Заказ не найден"
