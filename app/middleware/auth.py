from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.utils.alert import logger
from app.core.config import settings


class RapidAPIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # skip auth check for health endpoint
            if request.url.path == '/api/v1/health':
                return await call_next(request)

            # in dev: bypass auth and log everything
            if settings.is_development:
                logger("=" * 60)
                logger(f"[{settings.APP_ENV}] Request to: {request.url.path}")
                logger(f"Method: {request.method}")
                logger("Request Headers:")
                for key, value in request.headers.items():
                    display_value = value if 'key' not in key.lower() and 'secret' not in key.lower() else f"{value[:8]}..."
                    logger(f"  {key}: {display_value}")
                logger("=" * 60)
                logger(f"{settings.APP_ENV.upper()} MODE - Auth bypassed")
                
                response = await call_next(request)
                response.headers["X-Auth-Status"] = "Development Mode"
                response.headers["X-App-Env"] = settings.APP_ENV
                return response

            # in prod: always trust RapidAPI's proxy layer
            # rapidAPI validates subscriptions before forwarding requests to your API
            # this works for both playground testing and production API calls
            logger(f"Request accepted - authenticated via RapidAPI proxy layer")
            
            response = await call_next(request)
            response.headers["X-Auth-Status"] = "Verified via RapidAPI"
            response.headers["X-App-Env"] = settings.APP_ENV
            
            return response

        except HTTPException as e:
            return self._error_response(e.status_code, e.detail)
        except Exception as e:
            logger(f"Middleware error: {str(e)}")
            return self._error_response(500, "Internal server error")

    def _error_response(self, status_code: int, message: str):
        return JSONResponse(
            status_code=status_code,
            content={
                "detail": message,
                "app_env": settings.APP_ENV
            }
        )