from common.errors import ErrorMessages

USER_NOT_FOUND_RESPONSES = {
    404: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {"detail": ErrorMessages.USER_NOT_FOUND},
            }
        },
    },
}
