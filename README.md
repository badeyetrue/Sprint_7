# Финальный проект 7 спринта — Автотесты API Яндекс Самокат

Проект содержит автоматизированные тесты для проверки API учебного сервиса Яндекс Самокат с использованием Python, Pytest, Requests и Allure.

## Структура проекта
* `urls.py` — Локаторы URL и эндпоинты API.
* `data.py` — Ожидаемые сообщения об ошибках и тестовые данные.
* `conftest.py` — Фикстуры для подготовки (генерации) и автоматической очистки данных курьеров.
* `tests/` — Папка с тест-кейсами, разбитыми по функциональным возможностям (ручкам).

## Подготовка к запуску

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   venv\Scripts\activate     # Для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск тестов и генерация Allure-отчета

1. Запустите автотесты для сбора результатов Allure:
   ```bash
   pytest --alluredir=allure-results
   ```
2. Сгенерируйте HTML-отчет Allure:
   ```bash
   allure generate allure-results --clean -o allure-report
   ```
3. Откройте сформированный отчет в браузере:
   ```bash
   allure open allure-report
   ```
