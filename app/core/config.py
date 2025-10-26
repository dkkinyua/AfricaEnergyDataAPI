import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class CommonSettings(BaseSettings):
    APP_NAME: str = "africaenergyapi"
    VERSION: str = 'v1'
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("LOCAL_MONGO_URI")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
    API_KEY_TTL_SECONDS: int = 3600*24*30  # optional caching TTL

class DevSettings(CommonSettings):
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("LOCAL_MONGO_URI")

class TestSettings(CommonSettings):
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("PROD_MONGO_URI")

class ProdSettings(CommonSettings):
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("PROD_MONGO_URI")
    REDIS_URL: str = os.getenv("PROD_REDIS_URL")

def get_settings() -> CommonSettings:
    env = os.getenv("APP_ENV", "dev").lower()
    if env == "prod":
        return ProdSettings()
    if env == "test":
        return TestSettings()
    return DevSettings()

settings = get_settings()
