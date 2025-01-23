from typing import Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies.db import get_db
from app.core.schemas.users import User
from app.core.models.users import UserORM
from app.dependencies.auth import get_current_token_payload_user


async def get_current_active_auth_user(
        payload: dict = Depends(get_current_token_payload_user)
) -> User:
    phone_number: Optional[str] = payload.get("username")
    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phone number not found in token"
        )

    user_db = await get_user_by_phone_number(phone_number)

    user: User = User.from_orm(user_db)
    return user


async def get_user_by_phone_number(phone_number: str) -> User:
    async with get_db() as db:
        try:
            query = select(UserORM).where(UserORM.phone_number == phone_number)
            result = await db.execute(query)
            user_db = result.scalars().first()

            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            user = User.from_orm(user_db)
            return user

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while processing the request"
            )


async def check_seller_permissions(user: User = Depends(get_current_active_auth_user)):
    if not user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a seller to perform this action"
        )
    return user
