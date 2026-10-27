from typing import Any

import allure
import pytest
from pages.kinopoisk_page import KinopoiskPage
from selenium.webdriver.remote.webdriver import WebDriver

pytestmark = pytest.mark.ui


@allure.title("UI-01: Search film by Russian title")
@allure.story("Film search")
def test_search_russian(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.open()
    page.search(config["film"]["name"])
    page.wait_film_result()


@allure.title("UI-02: Search film by original title")
@allure.story("Film search")
def test_search_english(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.open()
    page.search(config["film"]["en_name"])
    page.wait_film_result()


@allure.title("UI-03: Film title and production year")
@allure.story("Film details")
def test_film_year(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.film()
    page.heading(f'{config["film"]["name"]} ({config["film"]["year"]})')


@allure.title("UI-04: Film director and genre")
@allure.story("Film details")
def test_film_credits(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.film()
    page.detail("Режиссер", config["person"]["name"])
    page.detail("Жанр", "фантастика")


@allure.title("UI-05: Director page from film card")
@allure.story("Person details")
def test_director_page(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.film()
    page.director()
    page.contains(config["person"]["en_name"])


@allure.title("UI-06: Film from person's best movies")
@allure.story("Person details")
def test_person_to_film(driver: WebDriver, config: dict[str, Any]) -> None:
    page = KinopoiskPage(driver, config)
    page.open(f'/name/{config["person"]["id"]}/')
    page.heading(config["person"]["name"])
    page.film_from_person()
