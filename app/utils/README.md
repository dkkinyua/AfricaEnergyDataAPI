## `utils/`

This folder contains utility functions for our API.

### `query.py`
This file contains the function `build_query()` which builds a MongoDB query dictionary based on filters entered by the user for example `year=2002`, `country=Kenya`, `start_year=2000&end_year=2010&unit=GWh`.

This query builder can be used across all routers for electricity, energy and socioeconomic endpoints.
