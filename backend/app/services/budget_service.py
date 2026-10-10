from decimal import Decimal


def calculate_food_budget(income: Decimal) -> Decimal:
    """
    Calculate the recommended monthly food budget.

    FoodWise currently uses 30% of monthly income
    as the baseline recommendation.
    """

    recommended_budget = income * Decimal("0.30")

    return recommended_budget.quantize(Decimal("0.01"))