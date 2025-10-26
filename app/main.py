from app.core.config import settings
from app.database.db import MongoDB
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.middleware.auth import RapidAPIKeyMiddleware, init_redis, redis_client
from app.routers import electricity, economic, energy
from app.utils.alert import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the database
    await MongoDB.connect()
    await init_redis()

    yield # the database stays on as long as the app is alive

    await MongoDB.close()
    if redis_client:
        await redis_client.close()
        logger("Redis connection closed successfully!")


app = FastAPI(
    lifespan = lifespan,
    title = settings.APP_NAME,
    version = settings.VERSION,
    description = "Africa Energy API to provide electricity, energy and socio-economic sector data for all 55 African Countries"
)

# setup routers
app.include_router(electricity.router, prefix="/api/v1/electricity", tags=["Electricity"])
app.include_router(economic.router, prefix="/api/v1/economic", tags=["Economic"])
app.include_router(energy.router, prefix="/api/v1/energy", tags=["Energy"])

# add middleware and test route
app.add_middleware(RapidAPIKeyMiddleware)

@app.get("/api/v1/health", include_in_schema=False)
def get_health():
    try:
        return {"detail": "API Health OK"}
    except Exception as e:
        return {"detail": f"Error: {e}"}