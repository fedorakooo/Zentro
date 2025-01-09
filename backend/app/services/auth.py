from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.dependencies.db import get_db
from app.core.models.users import users_table
from app.services import password_handler as auth_utils


async def validate_auth_users(phone_number: str, password: str):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid phone number or password"
    )

    async with get_db() as db:
        query = select(users_table).where(users_table.c.phone_number == phone_number)
        result = await db.execute(query)
        user = result.first()

        if not user:
            raise unauthed_exc

        if not auth_utils.validate_password(password, user.hashed_password):
            raise unauthed_exc

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user inactive"
            )

        return user
