from tasks.services import create_task, get_task_by_id


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


async def test_get_task_by_id(db_session, user):
    created = await create_task(
        session=db_session,
        user_id=user.id,
        title="Find me",
        description=None,
    )

    found = await get_task_by_id(
        session=db_session,
        task_id=created.id,
        user_id=user.id,
    )

    assert found.id == created.id
    assert found.title == "Find me"
