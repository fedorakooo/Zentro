from fastapi import APIRouter, Depends
from app.core.schemas.auth import TokenInfo
from app.services.auth import validate_auth_users
from app.core.schemas.users import UserLoginRequest
from app.services import jwt_manager

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserLoginRequest = Depends(validate_auth_users)):
    jwt_payload = {
        "phone_number": user.phone_number
    }
    token = jwt_manager.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
