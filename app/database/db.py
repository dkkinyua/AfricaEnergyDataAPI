from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

'''
this file allows for multiple mongodb connections across different routers e.g. electricity etc
avoids setting up the db each time in the router, while we can call them in different routes.
'''

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
        print(f"Connected to MongoDB: {cls.db.name}")

    @classmethod
    async def close(cls):
        """
        closes the MongoDB connection
        """
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed")

    @classmethod
    def get_collection(cls, name: str):
        """
        retrieves a MongoDB collection by name
        """
        if not cls.db:
            raise ConnectionError("Database connection not initialized. Call connect() first.")
        return cls.db[name]
