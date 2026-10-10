from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage, User
from app.schemas import FoodRecommendationResponse
from app.services.recommendation_service import recommend_food_package


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/food/{user_id}",
    response_model=FoodRecommendationResponse,
)
def get_food_recommendation(
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

    package, reason = recommend_food_package(
        user,
        packages,
    )

    return {
        "user_id": user.id,
        "recommended_package": package,
        "reason": reason,
    }