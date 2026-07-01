"""API endpoint tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import VALID_HOUSE


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"]


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_single(client: TestClient) -> None:
    response = client.post("/predict", json={"inputs": [VALID_HOUSE]})
    assert response.status_code == 200
    body = response.json()
    assert len(body["predictions"]) == 1
    assert body["predictions"][0]["predicted_value_usd"] > 0
    assert body["unit"] == "USD"


def test_predict_batch(client: TestClient) -> None:
    response = client.post("/predict", json={"inputs": [VALID_HOUSE, VALID_HOUSE]})
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2


def test_predict_rejects_missing_field(client: TestClient) -> None:
    bad = {k: v for k, v in VALID_HOUSE.items() if k != "MedInc"}
    response = client.post("/predict", json={"inputs": [bad]})
    assert response.status_code == 422


def test_predict_rejects_out_of_range(client: TestClient) -> None:
    bad = {**VALID_HOUSE, "Latitude": 999.0}
    response = client.post("/predict", json={"inputs": [bad]})
    assert response.status_code == 422


def test_predict_rejects_extra_field(client: TestClient) -> None:
    bad = {**VALID_HOUSE, "Unexpected": 1.0}
    response = client.post("/predict", json={"inputs": [bad]})
    assert response.status_code == 422


def test_predict_rejects_empty_batch(client: TestClient) -> None:
    response = client.post("/predict", json={"inputs": []})
    assert response.status_code == 422
