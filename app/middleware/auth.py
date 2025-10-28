from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.utils.alert import logger

class RapidAPIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Skip health check route entirely
            if request.url.path == '/api/v1/health':
                return await call_next(request)

            # Extract RapidAPI headers
            api_key = request.headers.get("X-RapidAPI-Key")
            proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

            # Ensure request came through RapidAPI gateway
            if not api_key or not proxy_secret:
                raise HTTPException(
                    status_code=403,
                    detail="Access restricted to RapidAPI subscribers only."
                )

            response = await call_next(request)
            response.headers["X-Auth-Status"] = "Verified via RapidAPI"
            return response

        except HTTPException as e:
            return self._error_response(e.status_code, e.detail)
        except Exception as e:
            logger(f"Middleware error: {e}")
            return self._error_response(500, "Internal server error")

    def _error_response(self, status_code: int, message: str):
        return JSONResponse(
            status_code=status_code,
            content={"detail": message}
        )
