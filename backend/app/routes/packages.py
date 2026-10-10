from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage
from app.schemas import FoodPackageResponse
from app.services.package_service import FOOD_PACKAGES


router = APIRouter(
    prefix="/packages",
    tags=["Food Packages"],
)


@router.get(
    "",
    response_model=list[FoodPackageResponse],
)
def list_food_packages(
    db: Session = Depends(get_db),
):
    packages = (
        db.query(FoodPackage)
        .order_by(FoodPackage.estimated_cost)
        .all()
    )

    return packages