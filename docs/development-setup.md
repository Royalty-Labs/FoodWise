# FoodWise Development Setup

This guide explains how to prepare a local development environment for FoodWise.

## Prerequisites

Install:

- Git
- Python
- Node.js and npm
- Access to a PostgreSQL database

## Clone the Repository

```powershell
git clone https://github.com/Royalty-Labs/FoodWise.git
cd FoodWise
```

If you already have a local copy of the repository, open PowerShell in that folder instead.

## Start the Backend

Open a terminal at the repository root.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and configure the database connection. Use the actual environment variables required by the application.

Apply migrations if configured:

```powershell
alembic upgrade head
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

The default local API documentation is available at `http://127.0.0.1:8000/docs`.

Keep this terminal running.

## Start the Frontend

Open a second terminal at the repository root.

```powershell
cd frontend
npm install
```

Create `frontend/.env.local` with the following configuration if the frontend uses this environment variable:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```powershell
npm run dev
```

Use the local URL printed by Vite.

## Environment Variables and Secrets

- Use `.env` for local backend configuration.
- Use `.env.local` for local frontend configuration where applicable.
- Never commit real credentials, database URLs containing passwords, or API keys.
- Remember that `VITE_` variables may be exposed to users in the browser.

## Deployment

- Frontend: https://foodwise-frontend.onrender.com
- Backend: https://foodwise-jum9.onrender.com
- API documentation: https://foodwise-jum9.onrender.com/docs

Local and deployed configurations may differ. Configure each environment independently.

## Related Guides

- [N-ATLaS Integration](n-atlas-integration.md)
- [Testing](testing.md)
- [Backend README](../backend/README.md)
- [Frontend README](../frontend/README.md)