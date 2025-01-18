from fastapi import APIRouter, Depends

from app.core.schemas.auth import TokenInfo
from app.services.auth.jwt_manager import encode_jwt
from app.core.schemas.users import UserLoginRequest
from app.services.auth.auth import validate_auth_users

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserLoginRequest = Depends(validate_auth_users)):
    jwt_payload = {
        "username": user.phone_number
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
