from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    username: str
    email: EmailStr


class CreateUserResponse(BaseModel):
    #success: bool
    user: UserData
