
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage, User
from app.schemas import (
    FoodAssistantChatResponse,
    FoodAssistantRequest,
    FoodPlanResponse,
)
from app.services.assistant_service import (
    generate_food_plan_message,
    understand_message,
)
from app.services.food_plan_service import create_food_plan

router = APIRouter(
    prefix="/assistant",
    tags=["Food Assistant"],
)


def _get_food_plan(
    user_id: str,
    db: Session,
    budget_limit=None,
    income_amount=None,
    household_size=None,
):
    """Create a food plan using the user's profile and optional overrides."""

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    packages = (
        db.query(FoodPackage)
        .order_by(FoodPackage.estimated_cost)
        .all()
    )

    if not packages:
        raise HTTPException(
            status_code=404,
            detail="No food packages available.",
        )

    try:
        return create_food_plan(
            user,
            packages,
            budget_limit=budget_limit,
            income_amount=income_amount,
            household_size=household_size,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post(
    "/food-plan",
    response_model=FoodPlanResponse,
)
def assistant_food_plan(
    request: FoodAssistantRequest,
    db: Session = Depends(get_db),
):
    """Return a structured food plan."""

    try:
        intent = understand_message(
            request.message,
            request.user_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if intent.intent not in {
        "get_food_plan",
        "show_food_plan",
        "adjust_food_budget",
    }:
        raise HTTPException(
            status_code=400,
            detail="Unsupported assistant intent.",
        )

    food_plan = _get_food_plan(
        user_id=intent.user_id,
        db=db,
        budget_limit=intent.budget_amount,
        income_amount=intent.income_amount,
        household_size=intent.household_size,
    )

    return food_plan


@router.post(
    "/chat",
    response_model=FoodAssistantChatResponse,
)
def assistant_chat(
    request: FoodAssistantRequest,
    db: Session = Depends(get_db),
):
    """Respond to food-planning requests in conversational form."""

    try:
        intent = understand_message(
            request.message,
            request.user_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if intent.intent not in {
        "get_food_plan",
        "show_food_plan",
        "adjust_food_budget",
    }:
        raise HTTPException(
            status_code=400,
            detail="Unsupported assistant intent.",
        )

    budget_limit = (
        intent.budget_amount
        if intent.intent == "adjust_food_budget"
        else None
    )

    food_plan = _get_food_plan(
        user_id=intent.user_id,
        db=db,
        budget_limit=budget_limit,
        income_amount=intent.income_amount,
        household_size=intent.household_size,
    )

    return FoodAssistantChatResponse(
        message=generate_food_plan_message(food_plan),
        food_plan=food_plan,
    )
