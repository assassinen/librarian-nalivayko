from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///library.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    # model = None

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(cls)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with new_session() as session:
            query = select(cls).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_uuid(cls, data_uuid: str):
        async with new_session() as session:
            query = select(cls).filter_by(uuid=data_uuid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with new_session() as session:
            async with session.begin():
                values.update(uuid=uuid4())
                new_instance = cls(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance


class TaskOrm(Base):
     __tablename__ = "tasks"
     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str]
     description: Mapped[str | None]


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    # TODO: добавлеть проверку на уникальность email
    email: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=True)

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_librarian: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(email={self.email})"


async def create_tables():
     async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
     async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.drop_all)
