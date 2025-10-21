import logging
from core.config import settings
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

'''
this file allows for multiple mongodb connections across different routers e.g. electricity etc
avoids setting up the db each time in the router, while we can call them in different routes.
'''
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect(cls):
        """
        initializes the MongoDB connection
        """
        cls.client = AsyncIOMotorClient(settings.DATABASE_URL)
        cls.db = cls.client.get_default_database()
        logger.info(f"MongoDB connection opened at {datetime.now(timezone.utc)}")

    @classmethod
    async def close(cls):
        """
        closes the MongoDB connection
        """
        if cls.client:
            cls.client.close()
            logger.info(f"MongoDB connection closed at {datetime.now(timezone.utc)}")

    @classmethod
    def get_collection(cls, name: str):
        """
        retrieves a MongoDB collection by name
        """
        if not cls.db:
            raise ConnectionError("Database connection not initialized. Call connect() first.")
        return cls.db[name]
