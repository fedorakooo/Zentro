from typing import Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, Row

from app.dependencies.db import get_db
from app.core.models.users import User
from app.dependencies.auth import get_current_token_payload_user


async def get_current_active_auth_user(
        payload: dict = Depends(get_current_token_payload_user)
) -> User:
    phone_number: Optional[str] = payload.get("phone_number")
    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phone number not found in token"
        )

    user = await get_user_by_phone_number(phone_number)
    return user


async def get_user_by_phone_number(phone_number: str) -> User:
    async with get_db() as db:
        query = select(User).where(User.phone_number == phone_number)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return user
