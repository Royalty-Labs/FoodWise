from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage, User
from app.schemas import FoodPlanResponse
from app.services.food_plan_service import create_food_plan


router = APIRouter(
    prefix="/food-plan",
    tags=["Food Plan"],
)


@router.get(
    "/{user_id}",
    response_model=FoodPlanResponse,
)
def get_food_plan(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
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

    return create_food_plan(
        user,
        packages,
    )