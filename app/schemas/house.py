"""Request/response schemas for the prediction API.

The feature set matches scikit-learn's California Housing dataset, where each row
describes a census *block group* (a small geographic area), not a single house.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# A realistic California block group, reused as an OpenAPI example.
_EXAMPLE = {
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.9841,
    "AveBedrms": 1.0238,
    "Population": 322.0,
    "AveOccup": 2.5556,
    "Latitude": 37.88,
    "Longitude": -122.23,
}


class HouseFeatures(BaseModel):
    """Features describing a single California census block group."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"example": _EXAMPLE})

    MedInc: float = Field(
        ..., gt=0, description="Median income in block group (tens of thousands USD)."
    )
    HouseAge: float = Field(
        ..., ge=0, le=100, description="Median house age in the block group (years)."
    )
    AveRooms: float = Field(..., gt=0, description="Average number of rooms per household.")
    AveBedrms: float = Field(..., gt=0, description="Average number of bedrooms per household.")
    Population: float = Field(..., ge=0, description="Block group population.")
    AveOccup: float = Field(..., gt=0, description="Average number of household members.")
    Latitude: float = Field(
        ..., ge=32, le=42, description="Block group latitude (California range)."
    )
    Longitude: float = Field(
        ..., ge=-125, le=-113, description="Block group longitude (California range)."
    )


class PredictionRequest(BaseModel):
    """A batch of one or more block groups to score."""

    model_config = ConfigDict(extra="forbid")

    inputs: list[HouseFeatures] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Between 1 and 1000 block groups to predict.",
    )


class Prediction(BaseModel):
    """A single predicted median house value."""

    predicted_value_usd: float = Field(..., description="Predicted median house value in USD.")


class PredictionResponse(BaseModel):
    """The response returned by the ``/predict`` endpoint."""

    predictions: list[Prediction]
    model_version: str
    unit: str = "USD"
