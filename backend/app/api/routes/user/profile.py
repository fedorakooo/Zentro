from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder

from app.core.schemas.users import User
from app.services.users.user import get_current_active_auth_user

router = APIRouter(tags=["Profile"], prefix="/user")


@router.get("/")
async def get_user_profile(user: User = Depends(get_current_active_auth_user)):
    return jsonable_encoder(user)
