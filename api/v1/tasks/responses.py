from http import HTTPStatus
from typing import Any

from common.errors import ErrorMessages

TASK_NOT_FOUND_RESPONSES: dict[int | str, dict[str, Any]] = {
    int(HTTPStatus.NOT_FOUND): {
        "description": "Задача не найдена",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.TASK_NOT_FOUND},
            }
        },
    },
}
