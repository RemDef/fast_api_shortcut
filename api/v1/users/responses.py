from http import HTTPStatus

from common.errors import ErrorMessages

USER_NOT_FOUND_RESPONSES = {
    HTTPStatus.NOT_FOUND: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.USER_NOT_FOUND},
            }
        },
    },
}
