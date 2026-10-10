from decimal import Decimal

from app.models import FoodPackage, User
from app.services.budget_service import calculate_food_budget
from app.services.recommendation_service import recommend_food_package


def create_food_plan(
    user: User,
    packages: list[FoodPackage],
):
    recommended_budget = calculate_food_budget(
        user.income_amount
    )

    package, reason = recommend_food_package(
        user,
        packages,
    )

    return {
        "user_id": user.id,
        "income_amount": user.income_amount,
        "household_size": user.household_size,
        "recommended_food_budget": recommended_budget,
        "recommended_package": package,
        "reason": reason,
    }