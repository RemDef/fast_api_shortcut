from uuid import UUID

from api.v1.tasks.get_list.query import TaskQuery

PREFIX = "tasks:list"


def tasks_list_key(user_id: UUID, query: TaskQuery) -> str:
    return (
        f"{PREFIX}:{user_id}:"
        f"limit={query.limit}"
        f"&offset={query.offset}"
        f"&is_done={query.is_done}"
        f"&created_from={query.created_from}"
        f"&created_to={query.created_to}"
        f"&order_by={query.order_by}"
        f"&direction={query.direction}"
        f"&search={query.search}"
    )


def tasks_list_pattern(user_id: UUID) -> str:
    return f"{PREFIX}:{user_id}:*"
