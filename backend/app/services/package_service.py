from decimal import Decimal

from app.models import FoodPackage


FOOD_PACKAGES = [
    {
        "name": "Basic Food Plan",
        "description": "A basic food plan for an individual or small household.",
        "package_type": "basic",
        "estimated_cost": Decimal("25000.00"),
        "household_size": 1,
        "duration_days": 30,
    },
    {
        "name": "Standard Food Plan",
        "description": "A balanced food plan for a small household.",
        "package_type": "standard",
        "estimated_cost": Decimal("45000.00"),
        "household_size": 3,
        "duration_days": 30,
    },
    {
        "name": "Family Food Plan",
        "description": "A larger food plan designed for a family household.",
        "package_type": "family",
        "estimated_cost": Decimal("75000.00"),
        "household_size": 5,
        "duration_days": 30,
    },
]


def seed_food_packages(db):
    existing_packages = db.query(FoodPackage).count()

    if existing_packages > 0:
        return

    for package_data in FOOD_PACKAGES:
        package = FoodPackage(**package_data)
        db.add(package)

    db.commit()