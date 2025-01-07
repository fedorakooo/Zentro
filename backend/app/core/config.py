import os

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# Project base directory
BASE_DIR = Path(__file__).parent.parent.parent


class DbSettings(BaseModel):
    host: str = os.environ.get("DB_HOST", "localhost")
    name: str = os.environ.get("DB_NAME", "default_db")
    user: str = os.environ.get("DB_USER", "user")
    password: str = os.environ.get("DB_PASS", "password")

    # Forming a URL for connecting to the database
    url: str = f"postgresql+asyncpg://{user}:{password}@{host}/{name}"
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
