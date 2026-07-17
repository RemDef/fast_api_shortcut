from common.errors import ErrorMessages

TASK_NOT_FOUND_RESPONSES = {
    404: {
        "description": "Задача не найдена",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.TASK_NOT_FOUND},
            }
        },
    },
}
