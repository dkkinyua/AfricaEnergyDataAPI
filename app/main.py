from app.core.config import settings
from contextlib import asynccontextmanager
from app.database.db import MongoDB
from fastapi import FastAPI
from app.routers import electricity, economic, energy

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the database
    await MongoDB.connect()

    yield # the database stays on as long as the app is alive

    await MongoDB.close()
    

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