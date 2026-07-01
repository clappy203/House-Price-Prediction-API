"""API routes."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from app.api.dependencies import get_model
from app.schemas.house import Prediction, PredictionRequest, PredictionResponse
from app.services.model import HousePriceModel

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", tags=["monitoring"], summary="Liveness / readiness probe")
def health(model: HousePriceModel = Depends(get_model)) -> dict[str, str]:
    """Return service health and the loaded model version."""
    return {"status": "ok", "model_version": model.version}


@router.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["predictions"],
    summary="Predict median house values",
)
def predict(
    payload: PredictionRequest,
    model: HousePriceModel = Depends(get_model),
) -> PredictionResponse:
    """Score a batch of block groups and return their predicted prices in USD."""
    values = model.predict(payload.inputs)
    logger.info("Scored %d block group(s)", len(values))
    return PredictionResponse(
        predictions=[Prediction(predicted_value_usd=round(value, 2)) for value in values],
        model_version=model.version,
    )
