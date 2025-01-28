from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import HTTPException

from app.core.models.users import UserORM
from app.core.schemas.users import UserUpdate
from app.dependencies.db import get_db
from app.services.auth.password_handler import validate_password


async def update_user_profile_db(
        user_id: int,
        user_update: UserUpdate
):
    async with get_db() as db:
        try:
            query = select(UserORM).where(UserORM.id == user_id)
            result = await db.execute(query)
            user_db = result.scalars().one_or_none()

            if not user_db:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )

            update_data = user_update.dict(exclude_unset=True)

            for key, value in update_data.items():
                setattr(user_db, key, value)

            await db.commit()
            await db.refresh(user_db)

            return {"message": "User updated successfully", "user_id": user_db.id}

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to update user due to a database error"
            )


async def delete_user_profile_db(
        user_id: int,
        password: str
):
    async with get_db() as db:
        try:
            query = select(UserORM).where(UserORM.id == user_id)
            result = await db.execute(query)
            user_db = result.scalars().one_or_none()

            if not user_db:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )

            if not validate_password(password, user_db.hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid password"
                )

            await db.delete(user_db)
            await db.commit()

            return {"message": "User deleted successfully", "user_id": user_db.id}

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete user")
