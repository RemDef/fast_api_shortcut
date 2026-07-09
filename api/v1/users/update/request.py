from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class UpdateUserRequest(BaseModel):
    username: Annotated[str | None, MinLen(3), MaxLen(20)] = None
    email: EmailStr | None = None
