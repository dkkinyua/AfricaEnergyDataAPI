## Core Configuration Module

This folder contains the core configuration logic for the **Africa Energy API**.  
It defines how environment-specific settings (development, testing, and production) are loaded and used across the application.

### File: `config.py`

The `config.py` file centralizes configuration management using **Pydantic**, **dotenv**, and **environment variables**.  
It ensures that all environment settings are loaded in a consistent and secure way.


### Features

-  Loads environment variables from a `.env` file automatically  
-  Uses **Pydantic**’s `BaseSettings` for type-safe configuration  
-  Supports multiple environments (`dev`, `test`, `prod`)  
-  Automatically selects the correct environment based on `APP_ENV`  
-  Provides default values for Redis and MongoDB URLs  
-  Centralized access to configuration via a single `settings` object  


### Configuration Classes

| Class | Description |
|-------|--------------|
| `CommonSettings` | Base configuration shared across all environments. Defines global variables like `APP_NAME`, `VERSION`, and `DATABASE_URL`. |
| `DevSettings` | Extends `CommonSettings` for local development with debugging enabled. |
| `TestSettings` | Used for testing. Disables debugging and points to a test database. |
| `ProdSettings` | Used for production with secure URLs and `DEBUG` turned off. |

---

### Environment Variables

Below are key environment variables that are in the `.env` file:

**NOTE: NEVER EVER hardcode environment variables or push your `.env` file to GitHub! Even at gunpoint!**

```bash
# General
APP_ENV=dev  # or test / prod

# MongoDB
LOCAL_MONGO_URI=mongodb://127.0.0.1:27017/africa_energy
PROD_MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/africa_energy

# Redis
LOCAL_REDIS_URL=redis://localhost:6379
PROD_REDIS_URL=redis://<production_redis_url>
```
### How It Works

- `.env` file is loaded using `dotenv`

- `get_settings()` reads `APP_ENV` from your environment

- Based on its value, one of the following is initialized:

    - `DevSettings()`

    - `TestSettings()`

    - `ProdSettings()`

The chosen configuration is stored in the global settings object

Any part of the API can import and use settings directly

### Example Integration

In the database setup in `database/db.py`:

```python
from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect(cls):
        cls.client = AsyncIOMotorClient(settings.DATABASE_URL)
        cls.db = client.get_default_database()
        print(f"Connected to {cls.db.name}")
```
### Switching Environments

In the `.env` file, change `APP_ENV` to the desired environment i.e. development, testing, and production as shown below

```ini
APP_ENV=dev # for development
APP_ENV=test # for testing
APP_ENV=prod # for production
```

### Summary
The `core/config.py` module ensures:

- Consistent configuration across environments

- Secure management of sensitive credentials

- Simple, readable code that follows the DRY and 12-Factor App principles