from fastapi import APIRouter
from fastapi.params import Depends, Form
from sqlalchemy import Delete

from app.core.schemas.users import User, UserUpdate
from app.services.user.profile import update_user_profile_db, delete_user_profile_db
from app.services.user.user import get_current_active_auth_user

router = APIRouter(tags=["Profile"], prefix="/profile")


@router.get("/", response_model=User)
async def get_user_profile(user: User = Depends(get_current_active_auth_user)):
    return user


@router.put("/update")
async def update_user_profile(
        user_update: UserUpdate,
        user: User = Depends(get_current_active_auth_user)
):
    result = await update_user_profile_db(
        user.id,
        user_update
    )
    return result


@router.delete("/delete")
async def delete_user(
        user: User = Depends(get_current_active_auth_user),
        user_password: str = Form(...)
):
    result = await delete_user_profile_db(
        user.id,
        user_password
    )

    return result
