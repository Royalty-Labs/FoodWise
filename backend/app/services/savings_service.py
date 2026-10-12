
from decimal import Decimal


def calculate_contribution(
    target_amount: Decimal,
    duration_months: int,
    contribution_frequency: str = "monthly",
) -> Decimal:
    """Calculate the planned contribution for the selected frequency."""

    if contribution_frequency == "daily":
        number_of_contributions = (
            Decimal(duration_months) * Decimal("365") / Decimal("12")
        )
    elif contribution_frequency == "weekly":
        number_of_contributions = (
            Decimal(duration_months) * Decimal("52") / Decimal("12")
        )
    elif contribution_frequency == "monthly":
        number_of_contributions = Decimal(duration_months)
    else:
        raise ValueError("Frequency must be daily, weekly, or monthly.")

    contribution = target_amount / number_of_contributions

    return contribution.quantize(Decimal("0.01"))
