
from decimal import Decimal

from app.models import FoodPackage, FoodPackageItem


FOOD_PACKAGES = [
    {
        "name": "Basic Food Plan",
        "description": "A sample food plan for one person.",
        "package_type": "basic",
        "estimated_cost": Decimal("25000.00"),
        "household_size": 1,
        "duration_days": 30,
    },
    {
        "name": "Standard Food Plan",
        "description": "A sample food plan for a household of three.",
        "package_type": "standard",
        "estimated_cost": Decimal("45000.00"),
        "household_size": 3,
        "duration_days": 30,
    },
    {
        "name": "Family Food Plan",
        "description": "A sample food plan for a household of five.",
        "package_type": "family",
        "estimated_cost": Decimal("75000.00"),
        "household_size": 5,
        "duration_days": 30,
    },
]


SAMPLE_PACKAGE_ITEMS = {
    "Basic Food Plan": [
        {"name": "Rice", "quantity": "2", "unit": "kg"},
        {"name": "Beans", "quantity": "1", "unit": "kg"},
        {"name": "Garri", "quantity": "1", "unit": "kg"},
        {"name": "Yam", "quantity": "2", "unit": "tubers"},
        {"name": "Vegetable oil", "quantity": "1", "unit": "litre"},
    ],
    "Standard Food Plan": [
        {"name": "Rice", "quantity": "5", "unit": "kg"},
        {"name": "Beans", "quantity": "3", "unit": "kg"},
        {"name": "Garri", "quantity": "3", "unit": "kg"},
        {"name": "Yam", "quantity": "4", "unit": "tubers"},
        {"name": "Vegetable oil", "quantity": "2", "unit": "litres"},
        {"name": "Tomatoes", "quantity": "2", "unit": "kg"},
        {"name": "Onions", "quantity": "1", "unit": "kg"},
    ],
    "Family Food Plan": [
        {"name": "Rice", "quantity": "10", "unit": "kg"},
        {"name": "Beans", "quantity": "5", "unit": "kg"},
        {"name": "Garri", "quantity": "5", "unit": "kg"},
        {"name": "Yam", "quantity": "8", "unit": "tubers"},
        {"name": "Vegetable oil", "quantity": "3", "unit": "litres"},
        {"name": "Tomatoes", "quantity": "3", "unit": "kg"},
        {"name": "Onions", "quantity": "2", "unit": "kg"},
        {"name": "Dried fish", "quantity": "1", "unit": "kg"},
    ],
}


def seed_food_packages(db):
    try:
        for package_data in FOOD_PACKAGES:
            package = (
                db.query(FoodPackage)
                .filter(
                    FoodPackage.name == package_data["name"]
                )
                .first()
            )

            if package is None:
                package = FoodPackage(**package_data)
                db.add(package)
                db.flush()

            if not package.items:
                for item_data in SAMPLE_PACKAGE_ITEMS[package.name]:
                    item = FoodPackageItem(
                        package_id=package.id,
                        name=item_data["name"],
                        quantity=Decimal(item_data["quantity"]),
                        unit=item_data["unit"],
                        estimated_unit_price=None,
                        price_checked_at=None,
                        verification_status="unverified",
                    )
                    db.add(item)

        db.commit()

    except Exception:
        db.rollback()
        raise
