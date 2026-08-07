from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.get_list.query import TaskQuery
from api.v1.tasks.get_list.response import PaginatedTasksResponse
from cache.backend import RedisCacheBackend
from cache.dependencies import get_cache
from common.pagination import page_url
from database import get_session
from tasks.cache_keys import tasks_list_key
from tasks.services import count_tasks, get_tasks

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedTasksResponse,
    summary="Получить список задач",
    description="Получает список задач текущего авторизованного пользователя.",
    response_description="Задачи получены",
)
async def get_tasks_endpoint(
    request: Request,
    query: Annotated[TaskQuery, Query()],
    user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    cache: RedisCacheBackend = Depends(get_cache),
) -> PaginatedTasksResponse:

    key = tasks_list_key(user_id, query)
    cached = await cache.get(key)
    if cached is not None:
        return PaginatedTasksResponse(**cached)

    tasks = await get_tasks(
        session=session,
        user_id=user_id,
        limit=query.limit,
        offset=query.offset,
        is_done=query.is_done,
        created_from=query.created_from,
        created_to=query.created_to,
        order_by=query.order_by,
        direction=query.direction,
        search=query.search,
    )
    total = await count_tasks(
        session=session,
        user_id=user_id,
        is_done=query.is_done,
        created_from=query.created_from,
        created_to=query.created_to,
        search=query.search,
    )

    next_offset = query.offset + query.limit
    next_url = (
        page_url(request, limit=query.limit, offset=next_offset)
        if next_offset < total
        else None
    )
    previous_url = (
        page_url(
            request,
            limit=query.limit,
            offset=max(query.offset - query.limit, 0),
        )
        if query.offset > 0
        else None
    )

    response = PaginatedTasksResponse(
        count=total,
        next=next_url,
        previous=previous_url,
        results=[TaskResponse.from_dto(dto=task) for task in tasks],
    )
    await cache.set(key, response.model_dump(mode="json"))
    return response
