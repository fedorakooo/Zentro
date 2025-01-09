from contextlib import asynccontextmanager
from app.core.db import async_session_maker


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
