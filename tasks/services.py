from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.errors import ErrorMessages
from .models import Task


async def create_task(
    session: AsyncSession, *, user_id: str, title: str, description: str | None
) -> Task:
    task = Task(title=title, description=description, user_id=user_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task_by_id(session: AsyncSession, *, task_id: str, user_id: str) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TASK_NOT_FOUND,
        )
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.NOT_THIS_USER_TASK,
        )
    return task


async def get_tasks(session: AsyncSession, *, user_id: str) -> list[Task]:
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return list(result.scalars().all())


async def update_task(
    session: AsyncSession,
    *,
    task_id: str,
    user_id: str,
    title: str | None = None,
    description: str | None = None,
    is_done: bool | None = None,
) -> Task:
    task = await get_task_by_id(session, task_id=task_id, user_id=user_id)

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if is_done is not None:
        task.is_done = is_done

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, *, task_id: str, user_id: str) -> None:
    task = await get_task_by_id(session, task_id=task_id, user_id=user_id)
    await session.delete(task)
    await session.commit()
