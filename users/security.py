import hashlib
import re
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 600_000)
    return f"{salt}:{digest.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    salt, digest_hex = hashed_password.split(":", 1)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 600_000)
    return secrets.compare_digest(digest.hex(), digest_hex)


def validate_password_strength(password: str) -> str:
    if not re.search(r"[a-z]", password):
        raise ValueError("Пароль должен содержать строчную букву")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Пароль должен содержать заглавную букву")
    if not re.search(r"\d", password):
        raise ValueError("Пароль должен содержать цифру")
    if not re.search(r"[^a-zA-Z0-9]", password):
        raise ValueError("Пароль должен содержать спецсимвол")
    return password
