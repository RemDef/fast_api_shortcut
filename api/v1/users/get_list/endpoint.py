from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import require_admin
from api.v1.users.common.schemas import UserResponse
from api.v1.users.get_list.query import UserQuery
from api.v1.users.get_list.response import PaginatedUsersResponse
from database import get_session
from users.dto import UserDTO
from users.services import count_users, get_users

router = APIRouter()


def _page_url(request: Request, *, limit: int, offset: int) -> str:
    query_params = dict(request.query_params)
    query_params["limit"] = str(limit)
    query_params["offset"] = str(offset)
    return str(request.url.replace(query=urlencode(query_params)))


@router.get(
    "/",
    response_model=PaginatedUsersResponse,
    summary="Получить пользователей",
    description="Получить список пользователей (только для админа).",
    response_description="Пользователи получены",
)
async def get_users_endpoint(
    request: Request,
    query: Annotated[UserQuery, Query()],
    _: UserDTO = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> PaginatedUsersResponse:
    users = await get_users(
        session=session,
        limit=query.limit,
        offset=query.offset,
    )
    total = await count_users(session=session)

    next_offset = query.offset + query.limit
    next_url = (
        _page_url(request, limit=query.limit, offset=next_offset)
        if next_offset < total
        else None
    )
    previous_url = (
        _page_url(
            request,
            limit=query.limit,
            offset=max(query.offset - query.limit, 0),
        )
        if query.offset > 0
        else None
    )

    return PaginatedUsersResponse(
        count=total,
        next=next_url,
        previous=previous_url,
        results=[
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                birthdate=user.birthdate,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ],
    )
