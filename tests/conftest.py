"""Shared pytest fixtures.

A real model is trained once per test session into a temporary directory, so the
suite exercises the genuine training + serving path end to end.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.ml.train import train

VALID_HOUSE = {
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.9841,
    "AveBedrms": 1.0238,
    "Population": 322.0,
    "AveOccup": 2.5556,
    "Latitude": 37.88,
    "Longitude": -122.23,
}


@pytest.fixture(scope="session")
def model_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Train a model once and return the artifact path."""
    path = tmp_path_factory.mktemp("artifacts") / "model.joblib"
    train(path)
    return path


@pytest.fixture(scope="session")
def client(model_path: Path) -> Iterator[TestClient]:
    """A TestClient wired to the freshly trained model."""
    app = create_app(Settings(model_path=model_path))
    with TestClient(app) as test_client:
        yield test_client
