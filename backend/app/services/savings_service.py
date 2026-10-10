from decimal import Decimal


def calculate_contribution(
    target_amount: Decimal,
    duration_months: int,
) -> Decimal:
    contribution = target_amount / Decimal(duration_months)

    return contribution.quantize(Decimal("0.01"))