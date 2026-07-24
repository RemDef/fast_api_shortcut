from fastapi import APIRouter

from api.v1.tasks.active_users.endpoint import router as active_users_router
from api.v1.tasks.create.endpoint import router as create_router
from api.v1.tasks.delete.endpoint import router as delete_router
from api.v1.tasks.get_by_id.endpoint import router as get_by_id_router
from api.v1.tasks.get_list.endpoint import router as read_tasks_router
from api.v1.tasks.stats.by_day.endpoint import router as stats_by_day_router
from api.v1.tasks.stats.total.endpoint import router as stats_total_router
from api.v1.tasks.update.endpoint import router as update_router

router = APIRouter(prefix="/tasks", tags=["tasks"])

router.include_router(create_router)
router.include_router(read_tasks_router)
router.include_router(stats_total_router)
router.include_router(stats_by_day_router)
router.include_router(active_users_router)
router.include_router(get_by_id_router)
router.include_router(update_router)
router.include_router(delete_router)
