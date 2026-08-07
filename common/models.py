from uuid import UUID, uuid4

from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
