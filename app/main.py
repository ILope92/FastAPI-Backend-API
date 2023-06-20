from fastapi import FastAPI
from app.core.exceptions import SettingNotFound
from app.core.init_app import (
    register_routers,
    init_middlewares,
    register_exceptions,
    configure_logging,
)

try:
    from app.settings.config import settings
except ImportError:
    raise SettingNotFound(
        "Can not import settings. Create settings file from template.config.py"
    )

docs_config = {
    "docs_url": "/api/docs/",
    "redoc_url": "/api/redocs/",
    "openapi_url": "/api/docs/openapi.json",
}

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.VERSION,
    **docs_config,
)

configure_logging()
register_routers(app)
init_middlewares(app)
register_exceptions(app)
