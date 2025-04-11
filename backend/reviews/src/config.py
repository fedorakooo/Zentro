import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseSettings:
    host: str = os.environ.get("DB_HOST")
    port: str = os.environ.get("DB_PORT")
    user: str = os.environ.get("DB_USER")
    name: str = os.environ.get("DB_NAME")
    password: str = os.environ.get("DB_PASS")

    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    pool_size: int = 5
    echo: bool = False


class Setting:
    db: DatabaseSettings = DatabaseSettings()


settings = Setting()
print(settings.db.url)
