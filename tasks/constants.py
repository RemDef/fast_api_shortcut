from tasks.models import Task

TASK_SORTABLE_FIELDS = {
    "created_at": Task.created_at,
    "updated_at": Task.updated_at,
    "title": Task.title,
}
