from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.users.models import User
from app.applications.users.schemas import (
    BaseUserCreate,
    BaseUserOut,
    BaseUserUpdate,
)
from app.core.auth.utils.contrib import (
    get_current_active_superuser,
    get_current_active_user,
)
from app.core.auth.utils.password import get_password_hash
from app.core.base.session import get_session

router = APIRouter()


@router.post(
    "/register",
    response_model=BaseUserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def register_user(
    user_in: BaseUserCreate,
    db_session: AsyncSession = Depends(get_session),
):
    """Register user.

    \nRaises:\n
        HTTPException (400): The user with this username already exists in
        the system

    \nReturns:\n
        Optional["User"]: Model user
    """
    user: Optional["User"] = await User.get_by_email_and_username(
        db_session=db_session,
        email=user_in.email,
        username=user_in.username,
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    password_hash: str = get_password_hash(user_in.password)
    created_user: Optional["User"] = await User.create(
        db_session=db_session, user=user_in, password_hash=password_hash
    )
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    return created_user


@router.post(
    "/create",
    response_model=BaseUserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def create_user(
    user_in: BaseUserCreate,
    db_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
):
    """Create new user.

    \nRaises:\n
        HTTPException (400): The user with this username already exists in
        the system

    \nReturns:\n
        Optional["User"]: Model user
    """
    user: Optional["User"] = await User.get_by_email_and_username(
        db_session=db_session,
        email=user_in.email,
        username=user_in.username,
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    password_hash: str = get_password_hash(user_in.password)
    created_user: Optional["User"] = await User.create(
        db_session=db_session, user=user_in, password_hash=password_hash
    )
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    return created_user


@router.get(
    "/",
    response_model=Optional[list[BaseUserOut]],
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def read_users(
    skip: int,
    limit: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
):
    """Retrive users

    \nArgs:\n
        • skip (int, optional): Skip result. Defaults to 0.\n
        • limit (int, optional): Max result. Defaults to 25.\n

    \nReturns:\n
        list: [User]
    """
    users: Optional[list["User"]] = await User.get_all_users(
        db_session=db_session,
        skip=skip,
        limit=limit,
    )
    if not users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users with such parameters were found",
        )
    return users


@router.get(
    "/get/me",
    response_model=BaseUserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    return current_user


@router.put(
    "/update/me",
    response_model=BaseUserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def update_user_me(
    user_in: BaseUserUpdate,
    current_user: User = Depends(get_current_active_user),
    db_session: AsyncSession = Depends(get_session),
):
    """
    Update own user.
    """
    if user_in.password is not None:
        password_hash = get_password_hash(user_in.password)
        current_user.password_hash = password_hash
    if user_in.username is not None:
        current_user.username = user_in.username
    if user_in.email is not None:
        current_user.email = user_in.email
    if user_in.first_name is not None:
        current_user.first_name = user_in.first_name
    if user_in.last_name is not None:
        current_user.last_name = user_in.last_name

    await current_user.save(db_session=db_session)
    return current_user


@router.get(
    "/get/{user_id}",
    response_model=BaseUserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db_session: AsyncSession = Depends(get_session),
):
    """
    Get a specific user by id.
    """
    user: Optional[User] = await User.get_user_for_id(
        db_session=db_session,
        id=user_id,
    )

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    if user == current_user:
        return user
    elif not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username does not exist in the system",
        )
    return user


@router.put(
    "/update/{user_id}",
    response_model=BaseUserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def update_user_by_id(
    user_id: int,
    user_in: BaseUserUpdate,
    current_user: User = Depends(get_current_active_superuser),
    db_session: AsyncSession = Depends(get_session),
):
    """
    Update a user by id.
    """
    user: Optional[User] = await User.get_user_for_id(
        db_session=db_session,
        id=user_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )

    await user.update_from_dict(
        data=user_in.create_update_dict(),
    )
    await user.save(db_session=db_session)

    return user


@router.delete(
    "/delete/{user_id}",
    response_model=BaseUserOut,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
async def delete_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db_session: AsyncSession = Depends(get_session),
):
    """
    Delete a user by id.
    """
    user: Optional[User] = await User.get_user_for_id(
        db_session=db_session,
        user_id=user_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    await user.delete(db_session=db_session)

    return user
