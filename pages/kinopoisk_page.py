"""Public read-only scenarios. No login, purchases or anti-bot bypass."""
from typing import Any

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class KinopoiskPage:
    def __init__(self, driver: WebDriver, config: dict[str, Any]) -> None:
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config["timeout_seconds"])

    @allure.step("Open public page: {path}")
    def open(self, path: str = "/") -> None:
        self.driver.get(self.config["ui_base_url"] + path)
        self.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
        if "captcha" in self.driver.current_url.lower():
            raise RuntimeError("UI automation blocked by CAPTCHA. No bypass attempted.")

    @allure.step("Search: {query}")
    def search(self, query: str) -> None:
        field = self.wait.until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, 'input[placeholder="Фильмы, сериалы, персоны"]'
        )))
        field.clear()
        field.send_keys(query)
        field.send_keys(Keys.ENTER)
        self.wait.until(ec.url_contains("/new-search/"))

    @allure.step("Find film link in search results")
    def wait_film_result(self) -> None:
        film_id = self.config["film"]["id"]
        self.wait.until(ec.visibility_of_element_located((
            By.CSS_SELECTOR, f'a[href="/film/{film_id}/"]'
        )))

    @allure.step("Wait for heading: {expected}")
    def heading(self, expected: str) -> None:
        self.wait.until(ec.text_to_be_present_in_element((By.TAG_NAME, "h1"), expected))

    @allure.step("Open configured film card")
    def film(self) -> None:
        self.open(f'/film/{self.config["film"]["id"]}/')
        self.heading(self.config["film"]["name"])

    @allure.step("Open director from film credits")
    def director(self) -> None:
        person_id = self.config["person"]["id"]
        self.wait.until(ec.element_to_be_clickable((
            By.CSS_SELECTOR, f'a[href="/name/{person_id}/"]'
        ))).click()
        self.heading(self.config["person"]["name"])

    @allure.step("Open film from person's best movies")
    def film_from_person(self) -> None:
        self.wait.until(ec.element_to_be_clickable((
            By.LINK_TEXT, self.config["film"]["name"]
        ))).click()
        self.heading(self.config["film"]["name"])

    @allure.step("Check page contains: {text}")
    def contains(self, text: str) -> None:
        self.wait.until(ec.text_to_be_present_in_element((By.TAG_NAME, "body"), text))
