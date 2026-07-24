from http import HTTPStatus

from common.errors import ErrorMessages

TASK_NOT_FOUND_RESPONSES = {
    HTTPStatus.NOT_FOUND: {
        "description": "Задача не найдена",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.TASK_NOT_FOUND},
            }
        },
    },
}
