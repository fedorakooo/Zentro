from fastapi import APIRouter, Depends
from app.core.schemas.auth import TokenInfo
from app.services.auth import validate_auth_users, jwt_manager
from app.core.schemas.users import UserLoginRequest

router = APIRouter(tags=["Authentication"])


@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserLoginRequest = Depends(validate_auth_users)):
    jwt_payload = {
        "username": user.phone_number
    }
    token = jwt_manager.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
