from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.services.jwt_manager import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_token_payload_user(
        token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )

    user_phone_number = payload.get("username")
    if not user_phone_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token does not contain user_phone_number"
        )

    return payload

