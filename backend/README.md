# FoodWise Backend

The FoodWise backend provides the API and server-side logic for the FoodWise application. It supports food budgeting, savings, food-plan recommendations, food packages, and assistant-related functionality.

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Psycopg
- Alembic
- Pydantic
- Uvicorn

## Prerequisites

Install the following before running the backend:

- Python
- PostgreSQL database access
- Git

## Local Setup

Run these commands from the root of the FoodWise repository.

### 1. Navigate to the backend directory

```powershell
cd backend
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and configure `DATABASE_URL` with your PostgreSQL connection string.

Example format:

```env
DATABASE_URL=postgresql+psycopg://username:password@host/database
```

Replace the example values with your actual database credentials. Do not commit `.env` or publish database credentials.

### 6. Apply database migrations

If Alembic is configured for your database, run:

```powershell
alembic upgrade head
```

### 7. Start the API server

```powershell
uvicorn app.main:app --reload
```

The local API should be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

## Project Organization

The backend includes application routes, services, and supporting configuration.

- `app/routes/` — API route modules.
- `app/services/` — application service logic.
- `app/` — application entry point and supporting modules.
- `alembic/` — database migration files, if present.
- `requirements.txt` — Python dependencies.
- `.env.example` — example environment configuration.

Refer to the actual repository structure when adding or modifying modules.

## Testing

Run the backend tests from the backend directory:

```powershell
python -m pytest
```

If pytest is not installed in the active environment, install it first:

```powershell
python -m pip install pytest
```

## Deployment

The deployed FoodWise backend is hosted at:

- **API:** https://foodwise-jum9.onrender.com
- **API documentation:** https://foodwise-jum9.onrender.com/docs

Deployment requires correctly configured environment variables and a working database connection.

## Security

- Keep database credentials and API keys private.
- Never commit `.env` files or other secrets.
- Validate incoming data and handle errors appropriately.
- Review authentication, authorization, and database access when changing API functionality.
- Do not assume that a feature is production-ready until it has been tested.

For the complete application overview and frontend setup, see the root `README.md`.