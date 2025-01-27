from fastapi import APIRouter

from app.dependencies.db import get_db
from app.core.schemas.users import UserRegisterRequest
from app.services.user.registration import register_user

router = APIRouter(tags=["Registration"])


@router.post("/register")
async def register(user: UserRegisterRequest):
    async with get_db() as db:
        response = await register_user(db, user)
        return response
