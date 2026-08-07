from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from users.dto import RegisterUserDTO, UserDTO
from users.exceptions import UserAlreadyExists, UserNotFoundError
from users.models import User
from users.security import hash_password, validate_password_strength, verify_password


def _to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        birthdate=user.birthdate,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_admin=user.is_admin,
    )


async def register_user(session: AsyncSession, *, data: RegisterUserDTO) -> User:
    validate_password_strength(data.password)

    user = User(
        username=data.username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        birthdate=data.birthdate,
        hashed_password=hash_password(data.password),
    )

    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists()

    await session.refresh(user)
    return user


async def get_users(
    session: AsyncSession,
    *,
    limit: int = 20,
    offset: int = 0,
) -> list[UserDTO]:
    result = await session.execute(
        select(User).order_by(User.username).limit(limit).offset(offset)
    )
    return [_to_dto(user) for user in result.scalars().all()]


async def count_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(User))
    return int(result.scalar_one())


async def _get_user_or_raise(session: AsyncSession, *, user_id: UUID) -> User:
    user: User | None = await session.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    return user


async def get_user_by_id(session: AsyncSession, *, user_id: UUID) -> UserDTO:
    user = await _get_user_or_raise(session, user_id=user_id)
    return _to_dto(user)


async def delete_user(session: AsyncSession, *, user_id: UUID) -> None:
    user = await _get_user_or_raise(session, user_id=user_id)
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
