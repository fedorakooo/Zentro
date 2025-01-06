from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.schemas.users import UserRegisterRequest
from app.services.registration import register_user

router = APIRouter()


@router.post("/register")
async def register(request: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        response = await register_user(db, request.email, request.phone_number, request.name, request.password)
        return response
    except HTTPException as e:
        raise e
