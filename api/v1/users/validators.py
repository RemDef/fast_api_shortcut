import re

from pydantic import SecretStr


def validate_password_strength(value: SecretStr) -> SecretStr:
    password = value.get_secret_value()
    if not re.search(r"[a-z]", password):
        raise ValueError("Пароль должен содержать строчную букву")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Пароль должен содержать заглавную букву")
    if not re.search(r"\d", password):
        raise ValueError("Пароль должен содержать цифру")
    if not re.search(r"[^a-zA-Z0-9]", password):
        raise ValueError("Пароль должен содержать спецсимвол")
    return value
