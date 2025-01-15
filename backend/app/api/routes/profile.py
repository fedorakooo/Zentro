from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.encoders import jsonable_encoder

from app.core.schemas.users import User
from app.services.user import get_current_active_auth_user

router = APIRouter(tags=["Profile"])


@router.get("/profile/")
async def get_profile(user: User = Depends(get_current_active_auth_user)):
    return jsonable_encoder(user)
