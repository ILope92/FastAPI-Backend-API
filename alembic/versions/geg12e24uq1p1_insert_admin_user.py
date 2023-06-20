"""insert admin user

Revision ID: geg12e24uq1p1
Revises: 9f45e4bae9af
Create Date: 2023-06-16 08:15:33.011231

"""
from alembic import op
from app.settings.config import settings
import datetime

# revision identifiers, used by Alembic.
revision = "geg12e24uq1p1"
down_revision = "9f45e4bae9af"


def upgrade() -> None:
    date_utc_now = datetime.datetime.utcnow()
    data = {
        "username": settings.__FIRST_ADMIN_LOGIN__,
        "password_hash": settings.__FIRST_ADMIN_PASSW__,
        "first_name": settings.__FIRST_ADMIN_LOGIN__,
        "last_name": settings.__FIRST_ADMIN_LOGIN__,
        "email": "admin@admin.com",
        "is_active": True,
        "is_superuser": True,
        "created_at": date_utc_now,
        "updated_at": date_utc_now,
    }

    keys: str = ",".join([key for key in data.keys()])
    values: str = ",".join([f"'{str(value) }'" for value in data.values()])
    sql_statement = f"INSERT INTO users ({keys}) VALUES ({values})"
    op.execute(sql_statement)


def downgrade() -> None:
    op.execute("DELETE FROM users;")
