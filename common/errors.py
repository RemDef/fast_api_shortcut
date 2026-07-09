from enum import StrEnum


class ErrorMessages(StrEnum):
    USER_NOT_FOUND = "Пользователь не найден"
    TASK_NOT_FOUND = "Задача не найдена"
    NOT_THIS_USER_TASK = "Нет доступа к этой задаче"
    INVALID_CREDENTIALS = "Неверный логин или пароль"
    INVALID_TOKEN = "Не удалось проверить учётные данные"
