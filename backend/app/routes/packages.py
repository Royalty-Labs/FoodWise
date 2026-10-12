
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodPackage, FoodPackageItem
from app.schemas import (
    FoodPackageItemCreate,
    FoodPackageResponse,
)


router = APIRouter(
    prefix="/packages",
    tags=["Food Packages"],
)


def set_contents_status(package: FoodPackage) -> None:
    if not package.items:
        package.contents_status = "not_defined"
    elif all(
        item.verification_status == "verified"
        for item in package.items
    ):
        package.contents_status = "verified"
    else:
        package.contents_status = "partially_verified"


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

    for package in packages:
        set_contents_status(package)

    return packages


@router.get(
    "/{package_id}",
    response_model=FoodPackageResponse,
)
def get_food_package(
    package_id: str,
    db: Session = Depends(get_db),
):
    package = (
        db.query(FoodPackage)
        .filter(FoodPackage.id == package_id)
        .first()
    )

    if package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food package not found.",
        )

    set_contents_status(package)
    return package


@router.post(
    "/{package_id}/items",
    response_model=FoodPackageResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_food_package_item(
    package_id: str,
    item_data: FoodPackageItemCreate,
    db: Session = Depends(get_db),
):
    package = (
        db.query(FoodPackage)
        .filter(FoodPackage.id == package_id)
        .first()
    )

    if package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food package not found.",
        )

    item = FoodPackageItem(
        package_id=package.id,
        name=item_data.name.strip(),
        quantity=item_data.quantity,
        unit=item_data.unit.strip(),
        estimated_unit_price=item_data.estimated_unit_price,
        verification_status="unverified",
    )

    db.add(item)
    db.commit()
    db.refresh(package)

    set_contents_status(package)
    return package
