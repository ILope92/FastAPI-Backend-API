from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.users.utils import update_last_login
from app.core.auth.schemas import JWTToken
from app.core.auth.utils.contrib import authenticate
from app.core.auth.utils.jwt import create_access_token
from app.core.base.session import get_session
from app.settings.config import settings

router = APIRouter()


@router.post("/access-token", response_model=JWTToken, tags=["login"])
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_session),
):
    user = await authenticate(
        db_session=db_session,
        username=form_data.username,
        password=form_data.password,
    )

    if user:
        await update_last_login(db_session=db_session, user_id=user.id)
    elif not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
