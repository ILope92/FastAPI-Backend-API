from sqlalchemy import Boolean, Column, String, DateTime
from app.core.base.base_models import BaseCreatedUpdatedAtModel, BaseDBModel
import datetime


class User(BaseDBModel, BaseCreatedUpdatedAtModel):
    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = {"extend_existing": True}
