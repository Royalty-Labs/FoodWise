# FoodWise

**Intelligent food planning, budgeting, savings, and access.**

FoodWise is a web application designed to help people make more informed food-budgeting decisions. It brings together food budgeting, savings tracking, food-plan recommendations, food packages, and an AI-assistant interface.

## Live Application

- **Frontend:** https://foodwise-frontend.onrender.com
- **Backend API:** https://foodwise-jum9.onrender.com
- **API Documentation:** https://foodwise-jum9.onrender.com/docs
- **GitHub:** https://github.com/Royalty-Labs/FoodWise

## Project Status

FoodWise has a deployed frontend and backend. N-ATLaS API integration and end-to-end model behaviour require verification before the integration can be described as fully operational.

## Features

- Food budgeting based on household needs and available income.
- Food-plan recommendations.
- Food-related savings tracking.
- Food package functionality.
- Food recommendations.
- An AI-assistant interface intended to support natural-language food-planning and budgeting interactions.

Feature availability depends on the current implementation and configuration. Live market prices, payment processing, delivery services, and fully operational AI responses should not be assumed unless implemented and verified.

## Technology Stack

**Frontend:** React, TypeScript, Vite, Lucide React.

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Psycopg, Alembic, and Pydantic.

**Deployment:** Render, with PostgreSQL hosting configured for the application.

## Project Structure

```text
FoodWise/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── config.py
│   │   └── database.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── docs/
└── README.md
```

## Getting Started

### Prerequisites

- Python compatible with the backend dependencies.
- Node.js and npm.
- Git.
- A PostgreSQL database.

### 1. Clone the repository

```powershell
git clone https://github.com/Royalty-Labs/FoodWise.git
cd FoodWise
```

### 2. Set up the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Configure the database connection in `backend/.env` using valid PostgreSQL credentials. Never commit your real `.env` file.

Apply database migrations:

```powershell
alembic upgrade head
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to inspect the API.

### 3. Set up the frontend

Open a second terminal at the repository root:

```powershell
cd frontend
npm install
```

Create `frontend/.env.local` with:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For the deployed backend, use:

```dotenv
VITE_API_BASE_URL=https://foodwise-jum9.onrender.com
```

Start the frontend:

```powershell
npm run dev
```

### 4. Run checks

From the frontend directory:

```powershell
npm run build
npm run lint
```

From the backend directory, with its virtual environment activated:

```powershell
python -m pip install pytest
python -m pytest
```

Document actual test results rather than assuming tests have passed.

## API Documentation

The backend contains route modules for users, budgets, savings, food plans, packages, recommendations, and the assistant.

Explore the deployed endpoints at:

https://foodwise-jum9.onrender.com/docs

## N-ATLaS Integration

FoodWise is designed to integrate N-ATLaS through a backend API architecture. The assistant service is responsible for processing requests, communicating with the configured model endpoint, and returning responses to the frontend.

API credentials must remain server-side and must never be committed to Git or exposed through frontend environment variables.

Verify successful live model responses, error handling, and response latency before describing the integration as fully operational.

## Security

- Never commit `.env` files, API keys, or database passwords.
- Do not commit local model weights or model caches.
- Use placeholder values in `.env.example`.
- Avoid logging secrets or sensitive user data.
- Configure CORS for the correct frontend origins.

## Contributing

Contributions and documentation improvements are welcome. Contribution guidelines will be added as the project documentation develops.

## Licence

A project licence has not yet been specified. Until the repository owner adds a licence, do not assume permission to reuse or redistribute the code.
