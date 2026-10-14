# FoodWise Frontend

The FoodWise frontend is the web interface for the FoodWise food-planning and budgeting application.

It provides the interface through which users can interact with food budgets, savings, food plans, recommendations, food packages, and the assistant.

## Technology Stack

- React
- TypeScript
- Vite
- Lucide React
- CSS and frontend assets

## Prerequisites

Before running the frontend locally, install:

- Node.js and npm
- Git

## Getting Started

### 1. Navigate to the frontend directory

```powershell
cd frontend
```

If you are already in the `frontend` directory, skip this command.

### 2. Install dependencies

```powershell
npm install
```

### 3. Configure the backend URL

Create a file named `.env.local` inside the `frontend` directory.

Add the following variable:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

This value assumes that the FoodWise backend is running locally on port `8000`. Use the appropriate backend URL if your configuration differs.

Do not place secret API keys or database credentials in frontend environment variables. Variables prefixed with `VITE_` can be exposed to the browser.

### 4. Start the development server

```powershell
npm run dev
```

Vite will display the local address where the frontend is available.

## Available Commands

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the development server |
| `npm run build` | Build the production frontend |
| `npm run lint` | Run the configured lint checks |
| `npm run preview` | Preview a production build locally |

Run these commands from the `frontend` directory.

## Backend Connection

The frontend communicates with the FoodWise backend API.

- **Live application:** https://foodwise-frontend.onrender.com
- **Live API:** https://foodwise-jum9.onrender.com
- **API documentation:** https://foodwise-jum9.onrender.com/docs

Local development requires the backend to be running and the frontend API URL to match the backend configuration.

## Development Notes

- Keep frontend components organized and reusable.
- Use TypeScript types to improve code clarity and catch errors.
- Avoid committing `.env.local` or other files containing secrets.
- Verify API responses and error handling when changing frontend-backend interactions.

For full project information, setup instructions, and architecture, see the root `README.md`.