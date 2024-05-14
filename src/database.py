from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import SQLALCHEMY_DATABASE_URL

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

SessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False  # влияет на возврат объекта при создании в БД с использованием session.flush()
)


class Base(DeclarativeBase):
    pass
