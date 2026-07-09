from fastapi import APIRouter
from api.v1.tasks.create.endpoint import router as create_router
from api.v1.tasks.get_list.endpoint import router as read_tasks_router
from api.v1.tasks.get_by_id.endpoint import router as get_by_id_router
from api.v1.tasks.update.endpoint import router as update_router
from api.v1.tasks.delete.endpoint import router as delete_router

router = APIRouter(prefix="/tasks", tags=["tasks"])


router.include_router(create_router)
router.include_router(get_by_id_router)
router.include_router(read_tasks_router)
router.include_router(update_router)
router.include_router(delete_router)
