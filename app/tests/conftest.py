import asyncio

import pytest_asyncio
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import alembic
from alembic.config import Config
from app.core.base.session import get_session
from app.settings.config import settings

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# NOT asyncpg
db_url_notasyncpg = settings.TEST_POSTGRES_DATABASE_URL.replace("+asyncpg", "")

# Create test database
create_engine_table = create_engine(db_url_notasyncpg)
if not database_exists(create_engine_table.url):
    create_database(create_engine_table.url)

db_url = settings.TEST_POSTGRES_DATABASE_URL
# Main engine and sessionmaker
engine = create_async_engine(db_url)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Alembic
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_section_option(
    alembic_cfg.config_ini_section,
    "sqlalchemy.url",
    db_url,
)
alembic.command.downgrade(alembic_cfg, "base")
alembic.command.upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_db_session() -> AsyncSession:
    async with engine.begin() as connection:
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture(scope="session")
async def async_client():
    app.dependency_overrides[get_session] = override_db_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def auth_headers_superuser(async_client: AsyncClient) -> dict[str, str]:
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"username": "admin", "password": "winsalg913tkwslkwq10q"},
    )
    response_json: dict = response.json()
    token: str = response_json.get("access_token")
    headers: dict = {"Authorization": f"bearer {token}"}
    return headers


@pytest_asyncio.fixture(scope="session")
async def auth_headers(async_client: AsyncClient) -> dict[str, str]:
    response = await async_client.post(
        "/api/auth/login/access-token",
        data={"username": "user", "password": "user"},
    )
    response_json: dict = response.json()
    token: str = response_json.get("access_token")
    headers: dict = {"Authorization": f"bearer {token}"}
    return headers
