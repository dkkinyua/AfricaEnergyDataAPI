from core.config import settings
from contextlib import asynccontextmanager
from database.db import MongoDB
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the database
    await MongoDB.connect()

    yield # the database stays on as long as the app is alive

    await MongoDB.close()
    

app = FastAPI(
    lifespan = lifespan,
    title = settings.APP_NAME,
    version = settings.version,
    description = "Africa Energy API to provide electricity, energy and socio-economic sector data for all 55 African Countries"
)
