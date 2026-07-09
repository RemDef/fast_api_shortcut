import hashlib
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 600_000)
    return f"{salt}:{digest.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    salt, digest_hex = hashed_password.split(":", 1)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 600_000)
    return secrets.compare_digest(digest.hex(), digest_hex)
