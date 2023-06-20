from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.base.session import get_session

import jwt
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.applications.users.models import User
from app.core.auth.schemas import JWTTokenPayload
from app.core.auth.utils.password import verify_and_update_password
from app.core.auth.utils.jwt import ALGORITHM
from app.settings.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token")


async def get_current_user(
    db_session: AsyncSession = Depends(get_session),
    token: str = Security(reusable_oauth2),
) -> Optional[User]:
    """_summary_

    Args:
        token (str, optional): _description_.
        Defaults to Security(reusable_oauth2).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Optional[User]: _description_
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = JWTTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await User.get_user_for_id(
        db_session=db_session,
        user_id=token_data.user_id,
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_superuser(
    current_user: User = Security(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_user(
    current_user: User = Security(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate(
    username: str,
    password: str,
    db_session: AsyncSession = Depends(get_session),
) -> Optional[User]:
    if username:
        user: Optional[User] = await User.get_by_username(
            db_session=db_session,
            username=username,
        )
    else:
        return None

    if user is None:
        return None

    verified, updated_password_hash = verify_and_update_password(
        password, user.password_hash
    )
    if not verified:
        return None

    if updated_password_hash is not None:
        user.password_hash = updated_password_hash
        await user.save(db_session=db_session)
    return user
