import os
import redis.asyncio as redis
from app.utils.alert import logger
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Optional

load_dotenv()

# cache duration
CACHE_TTL = 3600  

DEMO_KEY_1 = os.getenv("DEMO_KEY_1")
DEMO_KEY_2 = os.getenv("DEMO_KEY_2")

# Fallback valid keys
VALID_KEYS = {
    "demo-key-1",
    DEMO_KEY_1,
    "demo-key-2",
    DEMO_KEY_2,
}

redis_client: Optional[redis.Redis] = None

async def init_redis():
    """
    Initialize Redis connection once during FastAPI startup.
    """
    global redis_client
    try:
        redis_client = redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379"),
            encoding="utf-8",
            decode_responses=True
        )
        logger("Redis connected successfully.")
    except Exception as e:
        logger(f"Redis connection failed: {e}")
        redis_client = None


async def verify_key(api_key: str) -> bool:
    """
    Check Redis first, then fallback to VALID_KEYS.
    Cache valid keys in Redis for next time.
    """
    global redis_client
    try:
        if redis_client:
            cached_key = await redis_client.get(f"api_key:{api_key}")
            if cached_key == "valid":
                return True

        # Fallback to static valid keys
        if api_key in VALID_KEYS:
            if redis_client:
                await redis_client.setex(f"api_key:{api_key}", CACHE_TTL, "valid")
            return True

        return False

    except Exception as e:
        logger(f"Redis error: {e}")
        # fallback to static keys only when redis fails
        return api_key in VALID_KEYS


class RapidAPIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            api_key = (
                request.headers.get("x-rapidapi-key")
                or request.headers.get("x-api-key")
            )

            if not api_key:
                raise HTTPException(status_code=401, detail="Missing API key")

            is_valid = await verify_key(api_key)
            if not is_valid:
                raise HTTPException(status_code=403, detail="Invalid or Unauthorized API Key")
            
            response = await call_next(request)
            response.headers["X-Auth-Status"] = "Verified"
            return response
        # returns HTTP error responses
        except HTTPException as e:
            return self._error_response(e.status_code, e.detail)
        # returns server error responses
        except Exception as e:
            logger(f"Middleware error: {e}")
            detail = getattr(e, "detail", str(e))
            return self._error_response(500, detail)

    def _error_response(self, status_code: int, message: str):
        return JSONResponse(
            status_code= status_code,
            content = {"detail": message}
        )
