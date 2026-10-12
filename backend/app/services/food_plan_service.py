
from decimal import Decimal

from app.models import FoodPackage, User
from app.services.budget_service import calculate_food_budget
from app.services.recommendation_service import recommend_food_package


def create_food_plan(
    user: User,
    packages: list[FoodPackage],
    budget_limit: Decimal | None = None,
    income_amount: Decimal | None = None,
    household_size: int | None = None,
):
    effective_income = (
        income_amount
        if income_amount is not None
        else user.income_amount
    )
    effective_household_size = (
        household_size
        if household_size is not None
        else user.household_size
    )

    recommended_budget = (
        budget_limit
        if budget_limit is not None
        else calculate_food_budget(effective_income)
    )

    package, reason = recommend_food_package(
        user,
        packages,
        budget_limit=recommended_budget,
        income_amount=effective_income,
        household_size=effective_household_size,
    )

    return {
        "user_id": user.id,
        "income_amount": effective_income,
        "household_size": effective_household_size,
        "recommended_food_budget": recommended_budget,
        "recommended_package": package,
        "reason": reason,
    }
