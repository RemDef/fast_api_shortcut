from uuid import uuid4

import factory
from factory.alchemy import SQLAlchemyModelFactory

from tasks.models import Task
from users.dto import RegisterUserDTO
from users.models import User
from users.security import hash_password


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        session = cls._meta.sqlalchemy_session
        obj = model_class(*args, **kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def create_batch(cls, size, **kwargs):
        objects = []
        for _ in range(size):
            obj = await cls.create(**kwargs)
            objects.append(obj)
        return objects


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthdate = factory.Faker("date_of_birth", minimum_age=18, maximum_age=90)
    hashed_password = factory.LazyFunction(lambda: hash_password("Qwerty1!"))
    is_admin = False


class RegisterUserDTOFactory(factory.Factory):
    class Meta:
        model = RegisterUserDTO

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = "Qwerty1!"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthdate = factory.Faker("date_of_birth", minimum_age=18, maximum_age=90)


class TaskFactory(BaseFactory):
    class Meta:
        model = Task

    id = factory.LazyFunction(uuid4)
    title = factory.Sequence(lambda n: f"Task {n}")
    description = None
    is_done = False
    user_id = None
