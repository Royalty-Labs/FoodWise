from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SavingsGoal, User
from app.schemas import ( 
    SavingsGoalCreate, 
    SavingsGoalResponse, 
    SavingsProgressResponse, 
    SavingsContributionCreate, 
    SavingsContributionResponse )

from app.services.savings_service import calculate_contribution


router = APIRouter(
    prefix="/savings",
    tags=["Savings"],
)


@router.get(
    "/user/{user_id}",
    response_model=list[SavingsGoalResponse],
)
def get_user_savings_goals(
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

    goals = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.user_id == user_id)
        .all()
    )

    return goals



@router.post(
    "",
    response_model=SavingsGoalResponse,
    status_code=201,
)
def create_savings_goal(
    goal_data: SavingsGoalCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == goal_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    contribution_amount = calculate_contribution(
       goal_data.target_amount,
       goal_data.duration_months,
       goal_data.contribution_frequency,
    )

    goal = SavingsGoal(
        user_id=user.id,
        name=goal_data.name,
        target_amount=goal_data.target_amount,
        current_amount=Decimal("0.00"),
        duration_months=goal_data.duration_months,
        contribution_frequency=goal_data.contribution_frequency,
        contribution_amount=contribution_amount,
        status="active",
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


@router.get(
    "/{goal_id}/progress",
    response_model=SavingsProgressResponse,
)
def get_savings_progress(
    goal_id: str,
    db: Session = Depends(get_db),
):
    goal = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.id == goal_id)
        .first()
    )

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Savings goal not found.",
        )

    remaining_amount = max(
        goal.target_amount - goal.current_amount,
        Decimal("0.00"),
    )

    progress_percentage = (
        goal.current_amount / goal.target_amount
    ) * Decimal("100")

    progress_percentage = progress_percentage.quantize(
        Decimal("0.01")
    )

    return {
        "goal_id": goal.id,
        "goal_name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "remaining_amount": remaining_amount,
        "progress_percentage": progress_percentage,
        "status": goal.status,
    }



@router.post(
    "/{goal_id}/contributions",
    response_model=SavingsContributionResponse,
)
def add_savings_contribution(
    goal_id: str,
    contribution_data: SavingsContributionCreate,
    db: Session = Depends(get_db),
):
    goal = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.id == goal_id)
        .first()
    )

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Savings goal not found.",
        )

    if goal.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="This savings goal has already been completed.",
        )

    goal.current_amount += contribution_data.amount

    if goal.current_amount >= goal.target_amount:
        goal.current_amount = goal.target_amount
        goal.status = "completed"

    remaining_amount = max(
        goal.target_amount - goal.current_amount,
        Decimal("0.00"),
    )

    progress_percentage = (
        goal.current_amount / goal.target_amount
    ) * Decimal("100")
    
    progress_percentage = min(
        progress_percentage,
        Decimal("100.00"),
    ).quantize(Decimal("0.01"))

    db.commit()
    db.refresh(goal)

    return {
        "goal_id": goal.id,
        "goal_name": goal.name,
        "contribution_amount": contribution_data.amount,
        "current_amount": goal.current_amount,
        "target_amount": goal.target_amount,
        "remaining_amount": remaining_amount,
        "progress_percentage": progress_percentage,
        "status": goal.status,
    }