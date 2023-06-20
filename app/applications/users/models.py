from typing import Optional
from sqlalchemy import and_
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.base.base_models import BaseCreatedUpdatedAtModel, BaseDBModel
from app.applications.users.schemas import BaseUserCreate
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

    async def delete(self, db_session: AsyncSession) -> None:
        async with db_session as session:
            try:
                await session.delete(self)
                await session.commit()
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    async def update_from_dict(self, data: dict) -> "User":
        for key, value in data.items():
            setattr(self, key, value)
        return self

    async def save(self, db_session: AsyncSession) -> None:
        async with db_session as session:
            try:
                session.add(self)
                await session.commit()
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    @classmethod
    async def get_user_for_id(
        cls, db_session: AsyncSession, user_id: int
    ) -> Optional["User"]:
        async with db_session as session:
            query = select(cls).where(cls.id == user_id)
            try:
                result_get = await session.execute(query)
                return result_get.scalar_one_or_none()
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    @classmethod
    async def get_all_users(
        cls,
        db_session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Optional[list["User"]]:
        async with db_session as session:
            try:
                query = select(cls).limit(limit).offset(skip)

                list_users: Optional[list["User"]] = (
                    (await session.execute(query)).scalars().all()
                )
                if list_users:
                    return list_users
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    @classmethod
    async def get_by_email(
        cls,
        db_session: AsyncSession,
        email: str,
    ) -> Optional["User"]:
        async with db_session as session:
            try:
                query = select(cls).where(
                    cls.email == email,
                )
                find_user: tuple["User"] = await session.execute(query)
                find_user: User = find_user.scalar_one_or_none()
                if find_user:
                    return find_user
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    @classmethod
    async def get_by_email_and_username(
        cls,
        db_session: AsyncSession,
        email: str,
        username: str,
    ) -> Optional["User"]:
        async with db_session as session:
            try:
                query = select(cls).where(
                    and_(
                        cls.username == username,
                        cls.email == email,
                    )
                )
                result = await session.execute(query)
                find_user: User = result.scalar_one_or_none()
                if find_user:
                    return find_user
            except Exception:
                await session.rollback()
            finally:
                await session.close()

    @classmethod
    async def get_by_username(
        cls,
        db_session: AsyncSession,
        username: str,
    ) -> Optional["User"]:
        async with db_session as session:
            try:
                query = select(cls).where(
                    cls.username == username,
                )
                result = await session.execute(query)
                find_user: User = result.scalar_one_or_none()

                if find_user:
                    return find_user

            finally:
                await session.close()

    @classmethod
    async def create(
        cls,
        db_session: AsyncSession,
        user: BaseUserCreate,
        password_hash: str,
    ) -> Optional["User"]:
        model = cls(**user.to_dict_user(), password_hash=password_hash)

        async with db_session as session:
            try:
                session.add(model)
                await session.commit()
                return model
            except Exception:
                await session.rollback()
                return None
            finally:
                await session.close()
