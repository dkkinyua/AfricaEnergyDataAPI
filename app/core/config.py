import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = "africaenergyapi"
    VERSION: str = "v1"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("LOCAL_MONGO_URI")
    APP_ENV: str = os.getenv("APP_ENV", "dev")

    # Redis configs
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379") 
    UPSTASH_REDIS_REST_URL: str | None = os.getenv("UPSTASH_REDIS_REST_URL")
    UPSTASH_REDIS_REST_TOKEN: str | None = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    API_KEY_TTL_SECONDS: int = 3600 * 24 * 30

    @property
    def is_development(self) -> bool:
        """Check if app is in development mode"""
        return self.APP_ENV.lower() in ['dev', 'development']
    
    @property
    def is_production(self) -> bool:
        """Check if app is in production mode"""
        return self.APP_ENV.lower() in ['prod', 'production']


class DevSettings(CommonSettings):
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("LOCAL_MONGO_URI")
    APP_ENV: str = "dev"


class TestSettings(CommonSettings):
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("PROD_MONGO_URI")
    APP_ENV: str = "test"


class ProdSettings(CommonSettings):
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("PROD_MONGO_URI")
    APP_ENV: str = "prod"

    # using upstash-redis in production
    UPSTASH_REDIS_REST_URL: str = os.getenv("UPSTASH_REDIS_REST_URL")
    UPSTASH_REDIS_REST_TOKEN: str = os.getenv("UPSTASH_REDIS_REST_TOKEN")


def get_settings() -> CommonSettings:
    env = os.getenv("APP_ENV", "dev").lower()
    if env == "prod":
        return ProdSettings()
    if env == "test":
        return TestSettings()
    return DevSettings()


settings = get_settings()