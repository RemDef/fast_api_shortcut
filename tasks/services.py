from datetime import datetime
from typing import cast
from uuid import UUID

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.dto import ActiveUserDTO, TasksStatsByDayDTO, TasksStatsTotalDTO
from users.models import User

from .constants import TASK_SORTABLE_FIELDS
from .dto import TaskDTO
from .exceptions import TaskNotFoundError
from .models import Task

UNSET = object()


def _to_dto(task: Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


async def create_task(
    session: AsyncSession, *, user_id: UUID, title: str, description: str | None
) -> TaskDTO:

    task = Task(title=title, description=description, user_id=user_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return _to_dto(task)


async def _get_task_or_raise(
    session: AsyncSession, *, task_id: UUID, user_id: UUID
) -> Task:
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if task is None:
        raise TaskNotFoundError()
    return task


async def get_task_by_id(
    session: AsyncSession, *, task_id: UUID, user_id: UUID
) -> TaskDTO:
    task = await _get_task_or_raise(session, task_id=task_id, user_id=user_id)
    return _to_dto(task)


async def get_tasks(
    session: AsyncSession,
    *,
    user_id: UUID,
    limit: int = 20,
    offset: int = 0,
    is_done: bool | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    order_by: str = "created_at",
    direction: str = "desc",
    search: str | None = None,
) -> list[TaskDTO]:

    stmt = select(Task).where(Task.user_id == user_id)

    if is_done is not None:
        stmt = stmt.where(Task.is_done == is_done)
    if created_from is not None:
        stmt = stmt.where(Task.created_at >= created_from)
    if created_to is not None:
        stmt = stmt.where(Task.created_at <= created_to)

    search = search.lower().strip() if isinstance(search, str) else None
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Task.title.ilike(pattern),
                Task.description.ilike(pattern),
            )
        )

    column = TASK_SORTABLE_FIELDS[order_by]
    order_clause = column.desc() if direction == "desc" else column.asc()

    result = await session.execute(
        stmt.order_by(order_clause, Task.id).limit(limit).offset(offset)
    )

    return [_to_dto(task) for task in result.scalars().all()]


async def count_tasks(
    session: AsyncSession,
    *,
    user_id: UUID,
    is_done: bool | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    search: str | None = None,
) -> int:
    stmt = select(func.count()).select_from(Task).where(Task.user_id == user_id)

    if is_done is not None:
        stmt = stmt.where(Task.is_done == is_done)
    if created_from is not None:
        stmt = stmt.where(Task.created_at >= created_from)
    if created_to is not None:
        stmt = stmt.where(Task.created_at <= created_to)

    search = search.strip().lower() if search else None
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Task.title.ilike(pattern),
                Task.description.ilike(pattern),
            )
        )

    result = await session.execute(stmt)
    return int(result.scalar_one())


async def update_task(
    session: AsyncSession,
    *,
    task_id: UUID,
    user_id: UUID,
    title: str | None | object = UNSET,
    description: str | None | object = UNSET,
    is_done: bool | object = UNSET,
) -> TaskDTO:
    task = await _get_task_or_raise(session, task_id=task_id, user_id=user_id)

    if title is not UNSET:
        task.title = cast(str, title)
    if description is not UNSET:
        task.description = cast(str | None, description)
    if is_done is not UNSET:
        task.is_done = cast(bool, is_done)

    await session.commit()
    await session.refresh(task)
    return _to_dto(task)


async def delete_task(session: AsyncSession, *, task_id: UUID, user_id: UUID) -> None:
    task = await _get_task_or_raise(session, task_id=task_id, user_id=user_id)
    await session.delete(task)
    await session.commit()


async def get_tasks_stats_total(
    session: AsyncSession, *, user_id: UUID
) -> TasksStatsTotalDTO:
    stmt = select(
        func.count().label("total"),
        func.sum(case((Task.is_done.is_(True), 1), else_=0)).label("done"),
        func.sum(case((Task.is_done.is_(False), 1), else_=0)).label("not_done"),
    ).where(Task.user_id == user_id)
    row = (await session.execute(stmt)).one()
    total = int(row.total or 0)
    done = int(row.done or 0)
    not_done = int(row.not_done or 0)
    if total == 0:
        percent = 0.0
    else:
        percent = round(done * 100.0 / total, 2)
    return TasksStatsTotalDTO(
        total=total,
        done=done,
        not_done=not_done,
        completion_percent=percent,
    )


async def get_tasks_stats_by_day(
    session: AsyncSession, *, user_id: UUID
) -> list[TasksStatsByDayDTO]:
    day = func.date(Task.created_at)
    stmt = (
        select(
            day.label("day"),
            func.count().label("tasks_count"),
        )
        .where(Task.user_id == user_id)
        .group_by(day)
        .order_by(day.desc())
    )
    rows = (await session.execute(stmt)).all()
    return [TasksStatsByDayDTO(day=r.day, count=int(r.tasks_count)) for r in rows]


async def get_active_users(
    session: AsyncSession,
    *,
    limit: int = 10,
    offset: int = 0,
) -> list[ActiveUserDTO]:
    open_tasks = func.count(Task.id).label("open_tasks")
    stmt = (
        select(
            User.id.label("user_id"),
            User.username.label("username"),
            open_tasks,
        )
        .join(Task, Task.user_id == User.id)
        .where(Task.is_done.is_(False))
        .group_by(User.id, User.username)
        .order_by(open_tasks.desc(), User.username.asc())
        .limit(limit)
        .offset(offset)
    )
    rows = (await session.execute(stmt)).all()
    return [
        ActiveUserDTO(
            user_id=r.user_id,
            username=r.username,
            open_tasks=int(r.open_tasks),
        )
        for r in rows
    ]
