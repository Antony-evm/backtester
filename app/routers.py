"""
Define the routers for the FastAPI application.
"""
from fastapi import FastAPI

from modules.strategy_service.api.routes.trading_system_router import \
    trading_system_router


def include_routers(app: FastAPI):
    """
    Include all routers in the FastAPI application.
    """
    app.include_router(
        trading_system_router,
        prefix="/strategy-service/api/v1/trading-systems",
        tags=["trading-systems"]
    )