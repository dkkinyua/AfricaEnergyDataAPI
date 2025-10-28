from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.utils.alert import logger

class RapidAPIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # allow health check without headers
            if request.url.path == '/api/v1/health':
                return await call_next(request)

            # accept either header combination (for proxy or playground)
            api_key = request.headers.get("X-RapidAPI-Key") or request.headers.get("x-rapidapi-key")
            proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

            if proxy_secret and api_key:
                response = await call_next(request)
                response.headers["X-Auth-Status"] = "Verified via RapidAPI"
                return response

            if api_key:
                response = await call_next(request)
                response.headers["X-Auth-Status"] = "Verified via RapidAPI Playground"
                return response

            # block unauthorized requests
            raise HTTPException(
                status_code=403,
                detail="Access restricted to RapidAPI subscribers only. Please subscribe to a plan to access this endpoint"
            )

        except HTTPException as e:
            return self._error_response(e.status_code, e.detail)
        except Exception as e:
            print(f"Middleware error: {e}")
            return self._error_response(500, "Internal server error")

    def _error_response(self, status_code: int, message: str):
        return JSONResponse(
            status_code=status_code,
            content={"detail": message}
        )
