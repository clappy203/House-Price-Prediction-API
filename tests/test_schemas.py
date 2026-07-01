"""Schema validation tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.house import HouseFeatures
from tests.conftest import VALID_HOUSE


def test_valid_features() -> None:
    assert HouseFeatures(**VALID_HOUSE).MedInc == VALID_HOUSE["MedInc"]


def test_negative_income_rejected() -> None:
    with pytest.raises(ValidationError):
        HouseFeatures(**{**VALID_HOUSE, "MedInc": -1.0})


def test_extra_field_rejected() -> None:
    with pytest.raises(ValidationError):
        HouseFeatures(**{**VALID_HOUSE, "Unexpected": 1.0})
