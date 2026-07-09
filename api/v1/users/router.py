from fastapi import APIRouter
from api.v1.users.register.endpoint import router as register_router
from api.v1.users.get_list.endpoint import router as get_list_router
from api.v1.users.get_by_id.endpoint import router as get_by_id_router
from api.v1.users.update.endpoint import router as update_router
from api.v1.users.delete.endpoint import router as delete_router

router = APIRouter(prefix="/users", tags=["users"])


router.include_router(register_router)
router.include_router(get_list_router)
router.include_router(get_by_id_router)
router.include_router(update_router)
router.include_router(delete_router)
