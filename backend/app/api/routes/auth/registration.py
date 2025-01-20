from fastapi import APIRouter, HTTPException

from app.dependencies.db import get_db
from app.core.schemas.users import UserRegisterRequest
from app.services.user.registration import register_user

router = APIRouter(tags=["Registration"])


@router.post("/register")
async def register(request: UserRegisterRequest):
    async with get_db() as db:
        try:
            response = await register_user(db, request)
            return response
        except HTTPException as e:
            raise e
