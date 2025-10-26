## Database Module — Africa Energy API

This folder contains all the **database connection logic** used by the Africa Energy API.

It defines how the API connects to MongoDB in an **asynchronous**, **scalable**, and **reusable** manner using the `Motor` driver.

### Purpose of `db.py`

The `db.py` file provides a **centralized connection manager** for MongoDB.  
Instead of initializing a new connection in every router or service, we maintain a single shared client connection that can be accessed anywhere in the application.

This improves:
- Performance (no repeated connection overhead)
- Scalability (shared connection pool)
- Maintainability (one source of truth for database access)

### Main Components
- Motor — Asynchronous driver for MongoDB, enabling non-blocking I/O operations.

    - AsyncIOMotorClient — Provides connection pooling and high performance under concurrent loads.

- Environment Configuration — The MongoDB URI, `settings.DATABASE_URL` is managed via the central configuration file `core/config.py`.

### How It Works

###  Class: `MongoDB`

The `MongoDB` class encapsulates the logic for connecting to, closing, and retrieving MongoDB collections.

It uses **class methods** so that connections are managed at the class level — accessible throughout the entire app without creating multiple instances.


###  Class Methods Overview

| Method | Description |
|--------|--------------|
| `connect()` | Initializes an asynchronous connection to MongoDB using the URL in the `.env` file. It sets up both the client and the default database. |
| `close()` | Gracefully closes the MongoDB connection when the app shuts down. |
| `get_collection()` | Retrieves a specific MongoDB collection by name, ensuring the connection is already initialized. |


### Example Usage

**In your `main.py` (FastAPI app startup):**

```python
from fastapi import FastAPI
from database.db import MongoDB

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await MongoDB.close()
```

#### In a route in `electricity_routes.py`

```python
from fastapi import APIRouter, HTTPException
from database.db import MongoDB
from models.electricity_model import ElectricityModel

router = APIRouter()
collection = MongoDB.get_collection("electricity_data")

@router.get("/electricity/{country}")
async def get_electricity_per_country(country: str):
    try:
        # Retrieve all documents for the given country
        cursor = collection.find({"country": country})
        docs = list(cursor)  # Convert cursor to a list of documents

        if not docs:
            raise HTTPException(status_code=404, detail="No data found for this country")

        # Convert MongoDB documents to Pydantic models
        data = [ElectricityModel.from_db(doc) for doc in docs]

        return data

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

This design pattern ensures each route uses a shared MongoDB client without having to reinitialize a connection, while following the **Don't Repeat Yourself (DRY)** principle 