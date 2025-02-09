import string
import random

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

from app.core.models.users import UserORM
from app.core.schemas.users import UserRegisterRequest
from app.services.auth.password_handler import hash_password


async def register_user(db: AsyncSession, user: UserRegisterRequest):
    try:
        result = await db.execute(select(UserORM).filter(UserORM.email == user.email))
        existing_user = result.scalars().one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        result = await db.execute(select(UserORM).filter(UserORM.phone_number == user.phone_number))
        existing_user = result.scalars().one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is already registered"
            )

        referral_code = generate_referral_code()

        hashed_password = hash_password(user.password)

        new_user_data = {
            **user.dict(exclude={"password"}),
            "hashed_password": hashed_password,
            "referral_code": referral_code,
        }

        await db.execute(insert(UserORM).values(new_user_data))

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error occurred during user registration.",
            )

        return {"message": "User registered successfully", "phone_number": user.phone_number}

    except SQLAlchemyError as e:
        await db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred during user registration."
        )



def generate_referral_code(length=8):
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))
