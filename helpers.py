from faker import Faker

fake = Faker()

def get_random_courier_data(login=None, password=None, first_name=None):
    """Обычная функция-хелпер для генерации сырых данных.
    Изолирует примитивную логику Faker от фикстур pytest.
    """
    return {
        "login": login or fake.user_name(),
        "password": password or fake.password(length=10),
        "firstName": first_name or fake.first_name()
    }
