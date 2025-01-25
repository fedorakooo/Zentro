from fastapi import HTTPException, status, Form
from sqlalchemy import select

from app.core.schemas.users import UserLoginRequest
from app.dependencies.db import get_db
from app.core.models.users import UserORM
from app.services.auth import password_handler as auth_utils


async def validate_auth_users(
        username: str = Form(),
        password: str = Form()
) -> UserLoginRequest:
    unauthed_exc: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid phone number or password"
    )

    async with get_db() as db:
        # User login occurs using a phone number as username
        query = select(UserORM).where(UserORM.phone_number == username)
        result = await db.execute(query)
        user = result.scalars().one_or_none()

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
