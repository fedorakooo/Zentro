from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import settings

DATABASE_URL = settings.db.url

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


@asynccontextmanager
async def get_db():
    async with async_session_maker() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        else:
            await db.commit()
