from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists.",
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
        income_amount=user_data.income_amount,
        income_frequency=user_data.income_frequency,
        household_size=user_data.household_size,
        location=user_data.location,
        preferred_language=user_data.preferred_language,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user