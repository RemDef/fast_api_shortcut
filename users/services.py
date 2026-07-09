from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from common.errors import ErrorMessages
from users.security import hash_password, verify_password

from users.models import User


async def register_user(
    session: AsyncSession,
    *,
    username: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    birthdate: date,
) -> User:
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        birthdate=birthdate,
        hashed_password=hash_password(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.username))
    return list(result.scalars().all())


async def get_user_by_id(session: AsyncSession, *, user_id: str) -> User | None:
    return await session.get(User, user_id)


async def update_user(
    session: AsyncSession,
    *,
    user_id: str,
    username: str | None = None,
    email: str | None = None,
) -> User:
    user = await get_user_by_id(session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, *, user_id: str) -> None:
    user = await get_user_by_id(session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
    await session.delete(user)
    await session.commit()


async def authenticate_user(
    session: AsyncSession, *, username: str, password: str
) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
