
from decimal import Decimal

from app.models import FoodPackage, User
from app.services.budget_service import calculate_food_budget


def recommend_food_package(
    user: User,
    packages: list[FoodPackage],
) -> tuple[FoodPackage, str]:

    if not packages:
        raise ValueError(
            "No food packages are available for recommendation."
        )

    monthly_income = user.income_amount
    household_size = user.household_size

    # Use the shared budget calculation instead of duplicating it.
    recommended_budget = calculate_food_budget(monthly_income)

    # Prefer packages designed for the user's household size
    # or a larger household.
    suitable_packages = [
        package
        for package in packages
        if package.household_size >= household_size
    ]

    # If no package covers the household size, use the
    # packages designed for the largest available household.
    if not suitable_packages:
        largest_size = max(
            package.household_size for package in packages
        )

        suitable_packages = [
            package
            for package in packages
            if package.household_size == largest_size
        ]

    # Prefer a suitable package that does not exceed the budget.
    affordable_packages = [
        package
        for package in suitable_packages
        if package.estimated_cost <= recommended_budget
    ]

    if affordable_packages:
        # Select the most expensive affordable package.
        recommended_package = max(
            affordable_packages,
            key=lambda package: package.estimated_cost,
        )

        reason = (
            f"Based on your monthly income of "
            f"\u20A6{monthly_income:,.2f} and household size of "
            f"{household_size}, we recommend the "
            f"{recommended_package.name}. Its estimated cost is "
            f"\u20A6{recommended_package.estimated_cost:,.2f}, "
            f"which is within your recommended monthly food "
            f"budget of \u20A6{recommended_budget:,.2f}."
        )

    else:
        # No suitable package fits within the recommended budget.
        recommended_package = min(
            suitable_packages,
            key=lambda package: package.estimated_cost,
        )

        difference = (
            recommended_package.estimated_cost - recommended_budget
        )

        reason = (
            f"Based on your monthly income of "
            f"\u20A6{monthly_income:,.2f} and household size of "
            f"{household_size}, the "
            f"{recommended_package.name} is the lowest-cost "
            f"available package for your household needs. "
            f"Its estimated cost of "
            f"\u20A6{recommended_package.estimated_cost:,.2f} "
            f"exceeds your recommended monthly food budget of "
            f"\u20A6{recommended_budget:,.2f} by "
            f"\u20A6{difference:,.2f}."
        )

    # Explain when the available packages cannot cover everyone.
    if recommended_package.household_size < household_size:
        reason += (
            f" Note: this package is designed for "
            f"{recommended_package.household_size} people, "
            f"while your household has {household_size}. "
            f"A package sized for your full household is not "
            f"currently available."
        )

    return recommended_package, reason
