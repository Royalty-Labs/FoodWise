
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage, User
from app.schemas import FoodAssistantChatResponse, FoodAssistantRequest, FoodPlanResponse
from app.services.assistant_service import generate_food_plan_message, understand_message
from app.services.food_plan_service import create_food_plan


router = APIRouter(
    prefix="/assistant",
    tags=["Food Assistant"],
)


@router.post(
    "/food-plan",
    response_model=FoodPlanResponse,
)
def assistant_food_plan(
    request: FoodAssistantRequest,
    db: Session = Depends(get_db),
):
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

    if intent.intent != "get_food_plan":
        raise HTTPException(
            status_code=400,
            detail="Unsupported assistant intent.",
        )

    user = (
        db.query(User)
        .filter(User.id == intent.user_id)
        .first()
    )

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

    return create_food_plan(user, packages)



@router.post(
    "/chat",
    response_model=FoodAssistantChatResponse,
)
def assistant_chat(
    request: FoodAssistantRequest,
    db: Session = Depends(get_db),
):
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

    if intent.intent != "get_food_plan":
        raise HTTPException(
            status_code=400,
            detail="Unsupported assistant intent.",
        )

    user = (
        db.query(User)
        .filter(User.id == intent.user_id)
        .first()
    )

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

    food_plan = create_food_plan(user, packages)

    return FoodAssistantChatResponse(
        message=generate_food_plan_message(food_plan),
        food_plan=food_plan,
    )

