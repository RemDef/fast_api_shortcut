from uuid import UUID

from jose import JWTError, jwt

from config import settings


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


def get_user_id_from_token(token: str) -> UUID | None:
    try:
        payload = decode_access_token(token)
    except JWTError:
        return None

    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        return None

    try:
        return UUID(user_id)
    except ValueError:
        return None
