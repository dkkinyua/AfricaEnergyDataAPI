# AfricaEnergyDataAPI v1
This is the API for Africa Energy Data based on metrics, countries and units. Built by FastAPI for building endpoints, `pymongo`, Pydantic for data validation, `pytest` for testing middleware and API Key Authentication.

## Features

- Fast and asynchronous REST API using **FastAPI**
- Data endpoints for **Electricity**, **Energy**, and **Economic** indicators
- API key–based middleware authentication
- Pydantic validation for clean, structured data
- Comprehensive test coverage using **pytest**
- Easy deployment on **Render**, and **Docker**

## Contributions

Contributions are welcome! Whether it’s fixing a bug, improving documentation, or adding new features, your help is appreciated.

### How to Contribute

#### 1. **Fork the repository**
- Click the **Fork** button on the top right of this repository page.

#### 2. **Clone your fork**
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

#### 3. Create a new branch

```bash
git checkout -b feature/your-feature-name
```

#### 4. Make your changes

Follow the existing code style and structure.

Write or update tests if applicable.

Ensure all tests pass before pushing your code.

#### 5. Commit your changes
```bash
git commit -m "Add: your meaningful commit message"
```

#### 6. Push to your fork
```bash
git push origin feature/your-feature-name
```

#### 7. Create a Pull Request (PR)

Go to your fork on GitHub and click Compare & pull request.

Describe your changes clearly and submit the PR for review.

### Code Style Guidelines

- Follow PEP 8 for Python code formatting.

- Use type hints and docstrings for clarity.

- Keep functions short and focused on a single task.

- Avoid committing directly to the main branch.

### Reporting Issues

If you encounter a bug or have a feature suggestion, please open an issue:

- Go to the Issues tab.

- Describe the problem clearly and include reproduction steps if possible.

Thank you, your contributions help improve this project and make it more valuable for everyone.

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AfricaEnergyDataAPI.git
cd AfricaEnergyDataAPI
```

### 2. Create a Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate # Linux/MacOS 
myenv\Scripts\activate # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a .env file in the project root:

```ini
APP_ENV=dev
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>
DEMO_KEY_1=your_demo_api_key
# other env variables
```

### 5. Run the API Locally
```bash
uvicorn app.main:app --reload
```

By default, the server runs on:
http://127.0.0.1:8000

### 6. Running tests with `pytest`
FastAPI has a module `fastapi.testclient` which allows us to run tests in FastAPI on the fly using `pytest`

To run tests:
```bash
pytest -v
```

### 7. Run Docker Compose
In the same file location as `docker-compose.yml` file, run

```bash
docker compose up --build # For the first time, to install dependencies in requirements.txt

docker compose up -d # After building dependencies, run Docker in detach mode
```

## Endpoints and Example Requests.
### Endpoints 
The table below shows the list of the endpoints available in the API for fetching data per sector, checking API health, and testing API Key validation

The API provides access to structured datasets related to **electricity**, **energy**, and **economic** indicators across African countries.  
You can explore and test all endpoints interactively via the Swagger documentation below:

- **Swagger UI:** [https://localhost:8000/docs](https://localhost:8000/docs)  

| Endpoint | Method | Description | Required Query Parameters | Example Request |
|-----------|--------|--------------|----------------------------|-----------------|
| `/api/v1/electricity` | `GET` | Fetches electricity-related data for a given country, such as installed capacity, generation, and access metrics. | `country` *(string)* | `/api/v1/electricity?country=Kenya` |
| `/api/v1/energy` | `GET` | Retrieves general energy sector data for a specific country and sub-sector (e.g., access, efficiency, renewables). | `country` *(string)*, `sub_sector` *(string, optional)* | `/api/v1/energy?country=Egypt&sub_sector=Access` |
| `/api/v1/economic` | `GET` | Returns economic indicators (e.g., GDP, inflation, energy spending) for a given country and optional year range. | `country` *(string)*, `start_year` *(int, optional)*, `end_year` *(int, optional)* | `/api/v1/economic?country=South Africa&start_year=2000&end_year=2010` |
| `/api/v1/health` | `GET` | Health check endpoint to verify the API is running correctly. | None | `/api/v1/health` |


