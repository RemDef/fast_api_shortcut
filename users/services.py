from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.security import hash_password, verify_password
from users.dto import RegisterUserDTO
from users.exceptions import UserNotFoundError

from users.models import User


async def register_user(session: AsyncSession, *, data: RegisterUserDTO) -> User:
    user = User(
        username=data.username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        birthdate=data.birthdate,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.username))
    return list(result.scalars().all())


async def get_user_by_id(session: AsyncSession, *, user_id: str) -> User:
    user: User | None = await session.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    return user


async def delete_user(session: AsyncSession, *, user_id: str) -> None:
    user = await get_user_by_id(session, user_id=user_id)
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
