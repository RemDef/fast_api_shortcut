from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    birthdate: date
    created_at: datetime
    updated_at: datetime
