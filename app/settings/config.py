import os
from dotenv import load_dotenv
from app.core.auth.utils.password import get_password_hash

load_dotenv(".local.env")


class Settings:
    VERSION: str = "0.0.1"
    APP_TITLE: str = "DataGO Application"
    PROJECT_NAME: str = "DataGO Application"

    SERVER_HOST: str = os.getenv("SERVER_HOST")
    DEBUG: bool = True

    APPLICATIONS: list[str] = ["users"]

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    PROJECT_ROOT: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir),
    )
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")

    POSTGRES_DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    APPLICATIONS_MODULE: str = "app.applications"

    CORS_ORIGINS: list[str] = [
        f"http://{SERVER_HOST}",
        f"http://{SERVER_HOST}:8000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    __FIRST_ADMIN_LOGIN__: str = "admin"
    __FIRST_ADMIN_PASSW__: str = get_password_hash("winsalg913tkwslkwq10q")

    TEST_POSTGRES_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")


settings = Settings()
