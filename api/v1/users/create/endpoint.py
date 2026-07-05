from fastapi import APIRouter
from api.v1.users.create.request import CreateUserRequest
from api.v1.users.create.response import CreateUserResponse, UserData
from users.services import create_user

router = APIRouter()

@router.post("/", response_model=CreateUserResponse)
def create_user_endpoint(body: CreateUserRequest):
    result = create_user(username=body.username, email=body.email)
    return CreateUserResponse(
        success=result["success"],
        user=UserData(**result["user"]),
    )