from sqlalchemy import select

from tasks.models import Task
from tasks.services import create_task, get_task_by_id, get_tasks


async def test_create_task(db_session, user):
    task = await create_task(
        session=db_session,
        user_id=user.id,
        title="Service task",
        description="Created from service test",
    )

    assert task.title == "Service task"
    assert task.description == "Created from service test"
    assert task.is_done is False

    result = await db_session.execute(select(Task).where(Task.id == task.id))
    db_task = result.scalar_one()

    assert db_task.title == "Service task"
    assert db_task.description == "Created from service test"
    assert db_task.is_done is False
    assert db_task.user_id == user.id


async def test_get_tasks_list(db_session, user, tasks):
    result = await get_tasks(session=db_session, user_id=user.id)

    assert len(result) == 3
    returned_ids = {t.id for t in result}
    expected_ids = {task.id for task in tasks}
    assert returned_ids == expected_ids


async def test_get_task_by_id(db_session, user, task):
    found = await get_task_by_id(
        session=db_session,
        task_id=task.id,
        user_id=user.id,
    )

    assert found.id == task.id
    assert found.title == task.title
