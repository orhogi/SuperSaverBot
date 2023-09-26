from asyncio import current_task
from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

load_dotenv()
DB_URL = getenv('DB_URL')

engine = create_async_engine(
    DB_URL,
    future=True,
    echo=True,
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)
AsyncScopedSession = async_scoped_session(async_session, scopefunc=current_task)


# Dependency
async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()