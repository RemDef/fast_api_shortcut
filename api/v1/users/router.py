from fastapi import APIRouter
from api.v1.users.create.endpoint import router as create_router

router = APIRouter(prefix="/users", tags=["users"])
router.include_router(create_router)