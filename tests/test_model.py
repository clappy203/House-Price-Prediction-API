"""Model service tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.schemas.house import HouseFeatures
from app.services.model import HousePriceModel, ModelNotLoadedError
from tests.conftest import VALID_HOUSE


def test_load_missing_artifact_raises(tmp_path: Path) -> None:
    with pytest.raises(ModelNotLoadedError):
        HousePriceModel.load(tmp_path / "does-not-exist.joblib")


def test_predict_returns_positive_usd(model_path: Path) -> None:
    model = HousePriceModel.load(model_path)
    predictions = model.predict([HouseFeatures(**VALID_HOUSE)])
    assert len(predictions) == 1
    assert predictions[0] > 10_000  # sanity: a plausible house price in USD
