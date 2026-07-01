"""Application entrypoint and factory."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging
from app.services.model import HousePriceModel

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Load the model once at startup and attach it to the app state."""
    settings: Settings = app.state.settings
    app.state.model = HousePriceModel.load(settings.model_path)
    logger.info("Model %s ready", app.state.model.version)
    yield
    logger.info("Shutting down")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure a FastAPI application instance."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        summary="Predict California median house values from census block-group features.",
        lifespan=lifespan,
    )
    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["monitoring"], summary="Service metadata")
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "version": __version__, "docs": "/docs"}

    app.include_router(router)
    return app


app = create_app()
