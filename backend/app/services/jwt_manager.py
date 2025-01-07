import jwt

from typing import Optional, Union
from datetime import timedelta, datetime

from app.core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: Optional[timedelta] = None
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now
    )

    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token: Union[str, bytes],
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithm
    )
    return decoded
