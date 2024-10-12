# Задание для стажеров на позицию QA Auto/SDET
## Задание 1: Исследовательское тестирование
    1. Посетите сайт mts.ru и проведите мини-исследовательское тестирование.
    2. Опишите один тест-кейс, состоящий из 6-10 шагов, который должен включать взаимодействие со страницей и как минимум одну проверку (assert).

*Опишите два тест-кейса: позитивный и негативный сценарии.*

## Задание 2: Автоматизация тест-кейса
    1. На основе вашего тест-кейса создайте его автоматизацию.
    2. Используйте фреймворки Playwright и Pytest для создания UI-теста.
    3. Опишите комментариями каждый шаг.

*Для описания шагов используйте фреймворк Allure с его step-обертками.*

**Критерий оценки** *: Я должен иметь возможность запустить ваш тест локально. Тест должен открыть браузер, провести тестирование (успешно или неуспешно) и закрыться.*

## Задание 3: Написание простого сервера
### Напишите простой сервер, который может обрабатывать два маршрута:
    1. **/inverse** (метод POST): принимает JSON, меняет местами ключи и
    их значения, и возвращает ответ.
    **Пример:**
        ◦ Запрос:
        {"key1": "value1"}
        ◦ Ответ:
        {"value1": "key1"}
        ◦ Статус: 200
    2. **/unstable** (метод GET): с рандомной вероятностью возвращает:
    ◦ Код 200 и в ответе HAPPY
    ◦ Код 400 и в теле UNHAPPY

*Решение может быть реализовано с использованием любого фреймворка. 
*Скрипт должен запускаться одним файлом.*
*Реализуйте для вашего сервера Swagger. 
*Интерфейс должен открываться при запуске вашего сервера, 
*и с него должны корректно отправляться запросы на ваш сервер.*
*Напишите юнит-тесты для вашего сервера, используя Pytest.*

## Задание 4: Нагрузочное тестирование
    • Используя сервер из задания 3, напишите скрипт нагрузки.
    • Используйте инструменты Locust или K6.
    • Запустите на небольшом количестве пользователей для отладки,
    чтобы не перегрузить вашу машину.
    • Опишите ваши наблюдения: количество RPS, время отклика.
    
*Напишите скрипт sh/bat, который запустит сервер из задания 3, а затем запустит нагрузочный скрипт.*

*При запуске скрипта проведите мониторинг вашей системы на использование CPU и RAM, добавьте это в описание.*# MTS_Test_tasks_QA_Auto_SDET
