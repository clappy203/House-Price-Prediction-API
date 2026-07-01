"""Reproducible training pipeline for the California housing price model.

Run it with ``python -m app.ml.train`` (or ``make train``). It downloads the
California Housing dataset, fits a scaled gradient-boosting regressor, evaluates
it on a held-out split, and serializes an artifact bundle (estimator + metadata)
to disk for the API to load.
"""

from __future__ import annotations

import argparse
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app import __version__

logger = logging.getLogger(__name__)

RANDOM_STATE = 42
DEFAULT_OUTPUT = Path("artifacts/model.joblib")


def build_pipeline() -> Pipeline:
    """Return an unfitted preprocessing + model pipeline."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                GradientBoostingRegressor(
                    n_estimators=300,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def train(output_path: Path = DEFAULT_OUTPUT, test_size: float = 0.2) -> dict[str, float]:
    """Train, evaluate, and persist the model. Returns the evaluation metrics."""
    logger.info("Loading California Housing dataset...")
    dataset = fetch_california_housing()

    x_train, x_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=test_size, random_state=RANDOM_STATE
    )

    pipeline = build_pipeline()
    estimator_name = pipeline.named_steps["model"].__class__.__name__
    logger.info("Training %s on %d samples...", estimator_name, len(x_train))
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    metrics = {
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
        "rmse": round(float(mean_squared_error(y_test, predictions) ** 0.5), 4),
    }
    logger.info("Evaluation metrics (held-out test set): %s", metrics)

    bundle: dict[str, Any] = {
        "estimator": pipeline,
        "version": __version__,
        "metadata": {
            "trained_at": datetime.now(UTC).isoformat(),
            "dataset": "sklearn.datasets.fetch_california_housing",
            "features": list(dataset.feature_names),
            "target": "median_house_value (units of $100,000)",
            "estimator": estimator_name,
            "metrics": metrics,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, output_path)
    logger.info("Saved model artifact to %s", output_path)
    return metrics


def main() -> None:
    """CLI entrypoint."""
    logging.basicConfig(level="INFO", format="%(asctime)s | %(levelname)s | %(message)s")
    parser = argparse.ArgumentParser(description="Train the California housing price model.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Artifact output path.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Held-out test fraction.")
    args = parser.parse_args()
    train(args.output, args.test_size)


if __name__ == "__main__":
    main()
