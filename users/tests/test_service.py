from datetime import date

from users.dto import RegisterUserDTO
from users.security import verify_password
from users.services import authenticate_user, register_user


async def test_register_user_hashes_password(db_session):
    data = RegisterUserDTO(
        username="svc_user",
        email="svc_user@example.com",
        password="Qwerty1!",
        first_name="Svc",
        last_name="User",
        birthdate=date(1995, 1, 15),
    )
    user = await register_user(session=db_session, data=data)

    assert user.username == "svc_user"
    assert user.hashed_password != "Qwerty1!"
    assert verify_password("Qwerty1!", user.hashed_password) is True


async def test_authenticate_user_ok(db_session):
    data = RegisterUserDTO(
        username="svc_user2",
        email="svc_user2@example.com",
        password="Qwerty1!",
        first_name="Svc",
        last_name="User",
        birthdate=date(1995, 1, 15),
    )
    await register_user(session=db_session, data=data)

    user = await authenticate_user(
        session=db_session, username="svc_user2", password="Qwerty1!"
    )
    assert user is not None
    assert user.username == "svc_user2"
