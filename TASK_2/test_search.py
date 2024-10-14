import pytest
from playwright.sync_api import sync_playwright
import allure
import os

def start_search(page, step_title: str, search_ask:str):
    with allure.step("Открыть главную страницу MTS.ru"):
        page.goto("https://www.mts.ru")

    with allure.step("Нажать на иконку поиска"):
        page.get_by_text("Поиск").click()

    with allure.step(step_title):
        page.fill("input[name='q']", search_ask)

    with allure.step("Нажать клавишу Enter для выполнения поиска"):
        page.keyboard.press("Enter")
    

# Добавляем шаг для снятия скриншота
def take_screenshot(page, screenshot_name: str):
    screenshot_path = f"screenshots/{screenshot_name}.png"
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    page.screenshot(path=screenshot_path)
    with allure.step("Сделать скриншот"):
        allure.attach.file(screenshot_path, name=screenshot_name, attachment_type=allure.attachment_type.PNG)


@allure.title("TC001: Проверка поведения поиска при некорректном запросе")
@allure.description("Проверяем, что некорректный запрос '%%%%' возвращает сообщение об отсутствии результатов.")
def test_invalid_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        try:
            start_search(page,
                        "Ввести некорректный запрос '%%%%' в строку поиска", 
                        "%%%%")

            with allure.step("Проверить, что результаты поиска загрузились"):
                container_search = 'mts-search-content'
                page.wait_for_selector(container_search, timeout=5000)
                assert page.is_visible(container_search) == True, "Результаты поиска не отображаются."

            with allure.step("Проверить, что отображается сообщение 'Ничего не нашлось'"):
                page.wait_for_selector("text='Ничего не нашлось'", timeout=10000)
                assert page.locator("text='Ничего не нашлось'").is_visible(), "Сообщение 'Ничего не нашлось' не отображается."
            
            with allure.step("Проверить, что отображается сообщение 'Попробуйте изменить запрос'"):
                assert page.locator("text='Попробуйте изменить запрос'").is_visible(),"Сообщение 'Попробуйте изменить запрос' не отображается."
            
            take_screenshot(page, "invalid_search_result")
        finally:
            # Закрываем браузер
            browser.close()

# Позитивный тест-кейс для проверки успешного поиска
@allure.title("TC002: Проверка успешного поиска по валидному запросу")
@allure.description("Проверяем, что поиск с валидным запросом 'тарифы' возвращает корректные результаты.")
def test_valid_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        try:
            start_search(page,
                        "Ввести валидный запрос 'тарифы' в строку поиска", 
                        "тарифы")

            with allure.step("Дождаться загрузки страницы с результатами"):
                page.wait_for_selector(".mts-search__result-count", timeout=5000)  
                assert page.is_visible(".mts-search__result-count"), "Результаты поиска не отображаются."

            with allure.step("Проверка, что отображается сообщение с кол-вом найденных результатов"):
                search_result_text = page.locator(".mts-search__result-count").inner_text()
                assert "Найдено" in search_result_text, "Текст с количеством результатов не отображается."
                print(f"Текст с результатами: {search_result_text}")

            with allure.step("Проверка, что кол-во найденных результатов ненулевое"):
                search_res_count = int(page.locator("div.mts-search__result-count span").text_content())
                assert search_res_count != 0, "Кол-во найденных результатов нулевое"
            
            with allure.step("Проверка, что отображаются результаты поиска"):
                assert page.locator('div.mts-search__results').is_visible(), "Результаты поиска не отображаются"
         
            take_screenshot(page, "valid_search_result")
        finally:
            # Закрываем браузер
            browser.close()
 