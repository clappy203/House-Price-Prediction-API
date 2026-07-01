"""Model service: loads the serialized estimator and turns validated features
into human-readable price predictions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from app.schemas.house import HouseFeatures

logger = logging.getLogger(__name__)

#: Feature order expected by the trained estimator (matches sklearn's dataset).
FEATURE_ORDER: tuple[str, ...] = (
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
)

#: The California Housing target is expressed in units of $100,000.
TARGET_SCALE_USD = 100_000


class ModelNotLoadedError(RuntimeError):
    """Raised when the model artifact cannot be found or loaded."""


@dataclass
class HousePriceModel:
    """Thin wrapper around a fitted scikit-learn estimator."""

    estimator: Any
    version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> HousePriceModel:
        """Load a model bundle previously written by the training pipeline."""
        if not path.exists():
            raise ModelNotLoadedError(
                f"Model artifact not found at '{path}'. Run `make train` to create it."
            )
        bundle = joblib.load(path)
        logger.info("Loaded model artifact from %s", path)
        return cls(
            estimator=bundle["estimator"],
            version=bundle.get("version", "unknown"),
            metadata=bundle.get("metadata", {}),
        )

    def predict(self, houses: list[HouseFeatures]) -> list[float]:
        """Predict median house values (in USD) for a batch of block groups."""
        matrix = np.array(
            [[getattr(house, name) for name in FEATURE_ORDER] for house in houses],
            dtype=float,
        )
        raw_predictions = self.estimator.predict(matrix)
        return [float(value) * TARGET_SCALE_USD for value in raw_predictions]
