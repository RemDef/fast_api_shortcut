from fastapi import APIRouter
from api.v1.auth.login.endpoint import router as login_router

router = APIRouter(prefix="/auth", tags=["auth"])
router.include_router(login_router)
