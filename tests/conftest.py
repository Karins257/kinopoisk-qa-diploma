import json
import os
import platform
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import allure
import pytest
import requests
from secret import ApiKey
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture(scope="session")
def config() -> dict[str, Any]:
    source = Path(__file__).resolve().parents[1] / "config.json"
    return json.loads(source.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def token() -> ApiKey:
    value = os.getenv("POISKKINO_API_KEY", "").strip()
    if not value:
        pytest.fail("Set POISKKINO_API_KEY before running authenticated API tests")
    return ApiKey(value)


@pytest.fixture
def api() -> Iterator[requests.Session]:
    with requests.Session() as session:
        session.headers["Accept"] = "application/json"
        yield session


@pytest.fixture
def driver(config: dict[str, Any]) -> Iterator[WebDriver]:
    browser_name = os.getenv("BROWSER", "chrome")
    options: Options | FirefoxOptions = (
        FirefoxOptions() if browser_name == "firefox" else Options()
    )
    if config["headless"]:
        options.add_argument(
            "-headless" if browser_name == "firefox" else "--headless=new"
        )
    if browser_name == "chrome":
        options.add_argument("--window-size=1366,768")
    binary = os.getenv("CHROME_BINARY")
    if binary:
        options.binary_location = binary
    remote_url = os.getenv("WEBDRIVER_URL")
    if remote_url:
        instance = webdriver.Remote(command_executor=remote_url, options=options)
    elif browser_name == "firefox":
        instance = webdriver.Firefox(options=options)
    else:
        instance = webdriver.Chrome(options=options)
    instance.set_window_size(1366, 768)
    instance.set_page_load_timeout(config["timeout_seconds"])
    try:
        yield instance
    finally:
        try:
            links = instance.find_elements(
                By.CSS_SELECTOR, f'a[href="/film/{config["film"]["id"]}/"]'
            )
            diagnostic = {
                "url": instance.current_url,
                "title": instance.title,
                "browser": instance.capabilities.get("browserName"),
                "browser_version": instance.capabilities.get("browserVersion"),
                "platform": instance.capabilities.get("platformName"),
                "os_release": platform.freedesktop_os_release()
                if platform.system() == "Linux" else {"system": platform.platform()},
                "film_links": len(links),
                "visible_film_links": sum(link.is_displayed() for link in links),
                "headings": [
                    item.text
                    for item in instance.find_elements(By.CSS_SELECTOR, "h1,h2")
                ],
                "page_text_start": instance.find_element(
                    By.TAG_NAME, "body"
                ).text[:1200],
            }
            print("UI diagnostic: " + json.dumps(diagnostic, ensure_ascii=False))
            allure.attach(
                json.dumps(diagnostic, ensure_ascii=False, indent=2),
                "UI diagnostic", allure.attachment_type.JSON,
            )
            allure.attach(
                instance.get_screenshot_as_png(), "Browser state",
                allure.attachment_type.PNG,
            )
        except WebDriverException:
            pass
        instance.quit()
