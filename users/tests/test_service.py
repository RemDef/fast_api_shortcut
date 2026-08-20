from tests.factories import RegisterUserDTOFactory
from users.security import hash_password, verify_password
from users.services import authenticate_user, register_user


async def test_register_user_returns_dto(db_session):
    data = RegisterUserDTOFactory(username="svc_user", email="svc_user@example.com")
    user_dto = await register_user(session=db_session, data=data)

    for field in ("username", "email", "first_name", "last_name", "birthdate"):
        assert getattr(user_dto, field) == getattr(data, field)

    assert user_dto.is_admin is False
    assert user_dto.id is not None
    assert user_dto.created_at is not None
    assert user_dto.updated_at is not None


async def test_register_user_hashes_password_in_db(db_session):
    data = RegisterUserDTOFactory(username="svc_user2", email="svc_user2@example.com")
    user_dto = await register_user(session=db_session, data=data)

    from sqlalchemy import select

    from users.models import User

    result = await db_session.execute(select(User).where(User.id == user_dto.id))
    user_model = result.scalar_one()

    assert user_model.hashed_password != data.password
    assert verify_password(data.password, user_model.hashed_password)


async def test_authenticate_user_ok(db_session, user_factory):
    await user_factory.create(
        username="svc_user2",
        email="svc_user2@example.com",
        hashed_password=hash_password("Qwerty1!"),
    )

    found = await authenticate_user(
        session=db_session, username="svc_user2", password="Qwerty1!"
    )
    assert found is not None
    assert found.username == "svc_user2"
