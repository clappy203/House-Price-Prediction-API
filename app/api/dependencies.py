"""FastAPI dependencies."""

from __future__ import annotations

from typing import cast

from fastapi import Request

from app.services.model import HousePriceModel


def get_model(request: Request) -> HousePriceModel:
    """Return the model loaded once at application startup."""
    return cast(HousePriceModel, request.app.state.model)
