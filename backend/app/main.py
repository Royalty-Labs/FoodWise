from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.users import router as users_router
from app.routes.budgets import router as budgets_router
from app.routes.savings import router as savings_router
from app.database import SessionLocal
from app.services.package_service import seed_food_packages
from app.routes.packages import router as packages_router
from app.routes.recommendations import router as recommendations_router
from app.routes.food_plan import router as food_plan_router
from app.routes.assistant import router as assistant_router



app = FastAPI(
    title="FoodWise API",
    description="Intelligent food planning, savings and access.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://foodwise-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(budgets_router)
app.include_router(savings_router)
app.include_router(packages_router)
app.include_router(recommendations_router)
app.include_router(food_plan_router)
app.include_router(assistant_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to FoodWise",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.on_event("startup")
def startup():
    db = SessionLocal()

    try:
        seed_food_packages(db)
    finally:
        db.close()