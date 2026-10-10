from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodBudget, User
from app.schemas import FoodBudgetCreate, FoodBudgetResponse
from app.services.budget_service import calculate_food_budget


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
)


@router.post(
    "",
    response_model=FoodBudgetResponse,
    status_code=201,
)
def create_food_budget(
    budget_data: FoodBudgetCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == budget_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    recommended_amount = calculate_food_budget(
        user.income_amount
    )

    budget = FoodBudget(
        user_id=user.id,
        income_amount=user.income_amount,
        recommended_amount=recommended_amount,
        period="monthly",
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget