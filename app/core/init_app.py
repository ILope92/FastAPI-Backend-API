import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.applications.users.routes import router as users_router
from app.core.auth.routers.login import router as login_router
from app.core.exceptions import APIException, on_api_exception
from app.settings.log import DEFAULT_LOGGING
from app.settings.config import settings


def configure_logging(log_settings: dict = None):
    log_settings = log_settings or DEFAULT_LOGGING
    logging.config.dictConfig(log_settings)


def register_exceptions(app: FastAPI):
    app.add_exception_handler(APIException, on_api_exception)


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )


def register_routers(app: FastAPI):
    app.include_router(users_router, prefix="/api/auth/users")
    app.include_router(login_router, prefix="/api/auth/login")
