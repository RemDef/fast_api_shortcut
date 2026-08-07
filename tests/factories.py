from datetime import date
from uuid import uuid4

import factory

from tasks.models import Task
from users.models import User
from users.security import hash_password


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = "Test"
    last_name = "User"
    birthdate = date(1995, 1, 15)
    hashed_password = factory.LazyFunction(lambda: hash_password("Qwerty1!"))
    is_admin = False


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    id = factory.LazyFunction(uuid4)
    title = factory.Sequence(lambda n: f"Task {n}")
    description = None
    is_done = False
    user_id = None
