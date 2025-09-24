import uuid
from datetime import datetime, UTC

from sqlalchemy import DateTime, func, update as sqlalchemy_update, select, delete as sqlalchemy_delete, text, or_, \
    String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import class_mapper, DeclarativeBase, Mapped, mapped_column, declared_attr, \
    selectinload

from core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(self):

        _name = self.__name__
        _new_name = _name[0]
        for i in _name[1:]:
            if i.isupper():
                _new_name += '_'
            _new_name += i
        if _new_name[-1] == 'y':
            _new_name = _new_name[:-1] + 'ies'
        else:
            _new_name += 's'
        return _new_name.lower()


class Database:

    def __init__(self):
        self._engine = None
        self._session = None

    def init(self):
        self._engine = create_async_engine(settings.postgres_async_url)
        self._session = async_sessionmaker(self._engine, expire_on_commit=False)()

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as engine:
            await engine.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as engine:
            await engine.run_sync(Base.metadata.drop_all)

    @property
    def engine(self):
        return self._engine


db = Database()
db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()

    @classmethod
    async def create(cls, **kwargs):  # Create
        object_ = cls(**kwargs)  # noqa
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)  # noqa
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls)
        )
        new_obj = await db.execute(query)
        await cls.commit()
        return new_obj.scalar()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.id == id_)  # noqa
        return (await db.execute(query)).scalar()

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)  # noqa
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars()

    @classmethod
    async def filter(cls, criteria, *, relationship=None):
        query = select(cls).where(criteria)
        if relationship:
            query = query.options(selectinload(relationship))

        return (await db.execute(query)).scalars().all()

    async def search(cls, keyword: str):  # noqa
        string_columns = [
            prop.columns[0]
            for prop in class_mapper(cls).iterate_properties  # noqa
            if hasattr(prop, "columns") and isinstance(prop.columns[0].type, String)
        ]

        if not string_columns:
            raise ValueError(f"{cls.__name__} da String ustun yo'q.")

        query = select(cls).where(
            or_(*map(lambda col: col.ilike(f"%{keyword}%"), string_columns))
        )

        result = await db.execute(query)
        return result.scalars().all()


class Model(Base, AbstractClass):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    __abstract__ = True


class CreatedModel(Model):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=datetime.now(UTC))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


# TODO
async def get_session():
    yield db._session  # noqa
