from http import HTTPStatus
from typing import Any

from common.errors import ErrorMessages

USER_NOT_FOUND_RESPONSES: dict[int | str, dict[str, Any]] = {
    int(HTTPStatus.NOT_FOUND): {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.USER_NOT_FOUND},
            }
        },
    },
}
