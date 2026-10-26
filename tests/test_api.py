from typing import Any

import allure
import pytest
import requests
from secret import ApiKey

pytestmark = pytest.mark.api


def get_json(
    api: requests.Session, config: dict[str, Any], path: str,
    token_value: ApiKey | None, expected_status: int,
    params: dict[str, str | int] | None = None,
) -> dict[str, Any]:
    headers = {"X-API-KEY": token_value.value} if token_value else {}
    with allure.step(f"GET {path}"):
        response = api.get(
            f'{config["api_base_url"]}/{config["api_version"]}{path}',
            headers=headers, params=params, timeout=config["timeout_seconds"],
        )
        sanitized = (
            response.text.replace(token_value.value, "[REDACTED]")
            if token_value else response.text
        )
        allure.attach(sanitized, "Response body", allure.attachment_type.JSON)
    with allure.step(f"Check HTTP {expected_status} and JSON"):
        assert response.status_code == expected_status
        assert "application/json" in response.headers.get("Content-Type", "")
        return response.json()


@allure.title("API-01: Get film by ID")
@allure.story("Film API")
def test_film(api: requests.Session, config: dict[str, Any], token: ApiKey) -> None:
    film = config["film"]
    data = get_json(api, config, f'/movie/{film["id"]}', token, 200)
    with allure.step("Check film ID, name and year"):
        assert data["id"] == film["id"]
        assert data["name"] == film["name"]
        assert data["year"] == film["year"]


@allure.title("API-02: Search film by title")
@allure.story("Film API")
def test_movie_search(
    api: requests.Session, config: dict[str, Any], token: ApiKey,
) -> None:
    data = get_json(api, config, "/movie/search", token, 200, {
        "query": config["film"]["name"], "limit": 3,
    })
    with allure.step("Check expected film appears in results"):
        assert any(item["id"] == config["film"]["id"] for item in data["docs"])


@allure.title("API-03: Get person by ID")
@allure.story("Person API")
def test_person(api: requests.Session, config: dict[str, Any], token: ApiKey) -> None:
    person = config["person"]
    data = get_json(api, config, f'/person/{person["id"]}', token, 200)
    with allure.step("Check person ID and names"):
        assert data["id"] == person["id"]
        assert data["name"] == person["name"]
        assert data["enName"] == person["en_name"]


@allure.title("API-04: Search person by name")
@allure.story("Person API")
def test_person_search(
    api: requests.Session, config: dict[str, Any], token: ApiKey,
) -> None:
    data = get_json(api, config, "/person/search", token, 200, {
        "query": config["person"]["en_name"], "limit": 3,
    })
    with allure.step("Check expected person appears in results"):
        assert any(item["id"] == config["person"]["id"] for item in data["docs"])


@allure.title("API-05: Reject request without API key")
@allure.story("API validation")
def test_no_key(api: requests.Session, config: dict[str, Any]) -> None:
    data = get_json(api, config, f'/movie/{config["film"]["id"]}', None, 401)
    with allure.step("Check unauthorized error"):
        assert data["statusCode"] == 401
        assert data["error"] == "Unauthorized"


@allure.title("API-06: Reject zero page size")
@allure.story("API validation")
def test_invalid_limit(
    api: requests.Session, config: dict[str, Any], token: ApiKey,
) -> None:
    data = get_json(api, config, "/movie/search", token, 400, {
        "query": config["film"]["en_name"], "limit": 0,
    })
    with allure.step("Check input validation error"):
        assert data["statusCode"] == 400
        assert data["message"]
