## Models Module — Africa Energy API

This folder contains all the **data models** used across the Africa Energy API.

Each model defines the **structure**, **validation**, and **transformation** logic for the data served by the API.  
They are implemented using **Pydantic**, which provides robust data validation and type safety.

---

###  Purpose of Models

The models act as the **blueprint** for how data is represented in the API.  
They ensure that data coming from the database (MongoDB) is clean, standardized, and ready to be serialized as JSON for API consumers.

Each model (e.g., `ElectricityData`, `EnergyData`, `SocioEconomicData`) represents one data domain and defines:
- Core fields such as `country`, `metric`, `unit`, `sector`, etc.
- A dynamic `data` dictionary that stores year–value pairs (e.g., `2000: 5732`, `2001: 6010`, etc.)
- A utility class method `from_db()` that transforms MongoDB documents into the standardized API model

---

### Model Files Overview

| File | Description |
|------|--------------|
| `electricity.py` | Defines the data model for electricity-related statistics (electricity generation, installed capacity, etc.) |
| `energy.py` | Defines the data model for broader energy metrics like clean cooking energy across African countries |
| `socioeconomic.py` | Defines the data model for social and economic indicators relevant to energy development |

---

### The `from_db()` Class Method

MongoDB stores data in a flat format, where each year (`2000`, `2001`, `2024`, etc.) appears as a separate field in the document.  
The `from_db()` method is a **class-level function** that converts these raw documents into clean, structured API responses.

#### Importance of using `@classmethod`
This shows that the `from_db` method belongs to the class rather than an individual object instance.
So instead of calling `from_db` method this way:

```python
obj = ElectricityModel()
obj.from_db(doc)
```

We can call it directly on the class as so:

```python
ElectricityModel.from_db(doc)
```

It is cleaner and easier to call it in our routes.

###  Example

**Original MongoDB document from MongoDB:**
```json
{
  "country": "Kenya",
  "metric": "Electricity generation",
  "unit": "GWh",
  "sector": "Electricity",
  "sub_sector": "Generation",
  "source": "Africa Energy Portal",
  "2000": 5732,
  "2001": 6010,
  "2002": 6298,
  ...
  "2024": 14002
}
```

### Transformed Pydantic model after transformation by `from_db()` method:

``` json
{
  "country": "Kenya",
  "metric": "Electricity generation",
  "unit": "GWh",
  "sector": "Electricity",
  "sub_sector": "Generation",
  "source": "Africa Energy Portal",
  "data": {
    "2000": 5732,
    "2001": 6010,
    "2002": 6298,
    "2024": 14002
  }
}
```
This makes the API response consistent, human-readable, and developer-friendly, without modifying your original MongoDB structure.

### Benefits of This Approach
- Works directly with your existing MongoDB collections (no migrations needed)

- Keeps data models clean, modular, and scalable

- Provides a consistent API interface for developers

- Easily extendable to new data domains in the future (just add a new model file)