
def create_user(*, username: str, email: str) -> dict:
    return {"success": True, "user": {"username": username, "email": email}}

def get_users() -> list[dict]:
    return []