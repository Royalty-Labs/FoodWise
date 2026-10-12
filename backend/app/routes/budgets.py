
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodBudget, User
from app.schemas import (
    FoodBudgetCreate,
    FoodBudgetResponse,
    FoodBudgetUpdate,
)
from app.services.budget_service import calculate_food_budget


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
)


def get_latest_budget(db: Session, user_id: str):
    return (
        db.query(FoodBudget)
        .filter(FoodBudget.user_id == user_id)
        .order_by(
            FoodBudget.created_at.desc(),
            FoodBudget.id.desc(),
        )
        .first()
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
    user = db.query(User).filter(
        User.id == budget_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    recommended_amount = calculate_food_budget(
        user.income_amount
    )

    budget = get_latest_budget(db, user.id)

    if budget:
        # Refresh the recommendation without resetting
        # the user's chosen budget.
        budget.income_amount = user.income_amount
        budget.recommended_amount = recommended_amount
        budget.period = "monthly"
    else:
        # A new budget starts with the recommendation.
        budget = FoodBudget(
            user_id=user.id,
            income_amount=user.income_amount,
            recommended_amount=recommended_amount,
            budget_amount=recommended_amount,
            period="monthly",
        )
        db.add(budget)

    db.commit()
    db.refresh(budget)

    return budget


@router.get(
    "/user/{user_id}",
    response_model=FoodBudgetResponse | None,
)
def get_food_budget(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    # A user without a saved budget receives null.
    return get_latest_budget(db, user.id)


@router.put(
    "/user/{user_id}",
    response_model=FoodBudgetResponse,
)
def update_food_budget(
    user_id: str,
    budget_data: FoodBudgetUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    budget = get_latest_budget(db, user.id)

    if budget:
        budget.budget_amount = budget_data.budget_amount
        budget.income_amount = user.income_amount
        budget.recommended_amount = calculate_food_budget(
            user.income_amount
        )
        budget.period = "monthly"
    else:
        # Allow users to save a chosen budget before
        # requesting a recommendation.
        budget = FoodBudget(
            user_id=user.id,
            income_amount=user.income_amount,
            recommended_amount=calculate_food_budget(
                user.income_amount
            ),
            budget_amount=budget_data.budget_amount,
            period="monthly",
        )
        db.add(budget)

    db.commit()
    db.refresh(budget)

    return budget
