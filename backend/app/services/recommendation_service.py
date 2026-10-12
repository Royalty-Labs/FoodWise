
from decimal import Decimal

from app.models import FoodPackage, User
from app.services.budget_service import calculate_food_budget


def recommend_food_package(
    user: User,
    packages: list[FoodPackage],
    budget_limit: Decimal | None = None,
    income_amount: Decimal | None = None,
    household_size: int | None = None,
) -> tuple[FoodPackage, str]:
    if not packages:
        raise ValueError(
            "No food packages are available for recommendation."
        )

    monthly_income = (
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
        else calculate_food_budget(monthly_income)
    )

    suitable_packages = [
        package
        for package in packages
        if package.household_size >= effective_household_size
    ]

    # If no package accommodates the household, use the largest
    # available package rather than recommending an undersized one.
    if not suitable_packages:
        largest_size = max(
            package.household_size for package in packages
        )
        suitable_packages = [
            package
            for package in packages
            if package.household_size == largest_size
        ]

    affordable_packages = [
        package
        for package in suitable_packages
        if package.estimated_cost <= recommended_budget
    ]

    if affordable_packages:
        # Choose the smallest suitable package that fits the budget.
        package = min(
            affordable_packages,
            key=lambda item: (
                item.household_size,
                item.estimated_cost,
            ),
        )

        reason = (
            f"{package.name} costs ₦{package.estimated_cost:,.2f} "
            "and fits within your food budget for your household size."
        )

        return package, reason

    # No suitable package is affordable: recommend the cheapest
    # suitable option and explain that it exceeds the budget.
    package = min(
        suitable_packages,
        key=lambda item: item.estimated_cost,
    )

    reason = (
        f"{package.name} is the cheapest suitable option available, "
        "but its cost is above your limit."
    )

    return package, reason
