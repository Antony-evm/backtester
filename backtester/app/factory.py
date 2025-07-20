"""
Factory for creating the FastAPI application instance.
"""
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from backtester.app.exceptions import http_exception_handler
from backtester.app.routers import include_routers


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    :return: FastAPI application instance
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routers(app)
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app
