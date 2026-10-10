from decimal import Decimal

import pytest

from app.models import FoodPackage, User
from app.services.budget_service import calculate_food_budget
from app.services.recommendation_service import recommend_food_package
from app.services.food_plan_service import create_food_plan
from app.services.assistant_service import understand_message

def make_user(income, household_size):
    return User(
        income_amount=Decimal(income),
        household_size=household_size,
    )


def make_package(name, cost, household_size):
    return FoodPackage(
        name=name,
        description=f"{name} description",
        package_type="standard",
        estimated_cost=Decimal(cost),
        household_size=household_size,
        duration_days=30,
    )



def test_understand_food_plan_request():
    result = understand_message(
        "Show me my food plan",
        "test-user",
    )

    assert result.intent == "get_food_plan"
    assert result.user_id == "test-user"


def test_understand_food_budget_request():
    result = understand_message(
        "What's my food budget?",
        "test-user",
    )

    assert result.intent == "get_food_plan"


def test_reject_unsupported_request():
    with pytest.raises(ValueError, match="couldn't identify"):
        understand_message(
            "Tell me a joke",
            "test-user",
        )


def test_calculate_food_budget():
    result = calculate_food_budget(Decimal("150000"))

    assert result == Decimal("45000.00")


def test_recommend_affordable_package_for_household():
    user = make_user("150000", 3)

    packages = [
        make_package("Basic Food Plan", "25000", 1),
        make_package("Standard Food Plan", "45000", 3),
        make_package("Family Food Plan", "75000", 5),
    ]

    package, reason = recommend_food_package(user, packages)

    assert package.name == "Standard Food Plan"
    assert package.estimated_cost == Decimal("45000.00")
    assert "Standard Food Plan" in reason


def test_recommend_cheapest_suitable_package_when_budget_is_too_low():
    user = make_user("50000", 3)

    packages = [
        make_package("Standard Food Plan", "45000", 3),
        make_package("Family Food Plan", "75000", 5),
    ]

    package, reason = recommend_food_package(user, packages)

    assert package.name == "Standard Food Plan"
    assert "exceeds" in reason.lower()


def test_recommend_largest_available_package_for_large_household():
    user = make_user("300000", 10)

    packages = [
        make_package("Basic Food Plan", "25000", 1),
        make_package("Standard Food Plan", "45000", 3),
        make_package("Family Food Plan", "75000", 5),
    ]

    package, reason = recommend_food_package(user, packages)

    assert package.name == "Family Food Plan"
    assert package.household_size == 5


def test_no_packages_raises_error():
    user = make_user("150000", 3)

    with pytest.raises(ValueError, match="No food packages"):
        recommend_food_package(user, [])


def test_create_food_plan_returns_complete_plan():
    user = make_user("150000", 3)

    packages = [
        make_package("Basic Food Plan", "25000", 1),
        make_package("Standard Food Plan", "45000", 3),
        make_package("Family Food Plan", "75000", 5),
    ]

    result = create_food_plan(user, packages)

    assert result["income_amount"] == Decimal("150000")
    assert result["household_size"] == 3
    assert result["recommended_food_budget"] == Decimal("45000.00")

    assert result["recommended_package"].name == "Standard Food Plan"

    assert "Standard Food Plan" in result["reason"]
    assert "₦45,000.00" in result["reason"]



def test_understand_natural_food_planning_request(monkeypatch):
    import app.services.assistant_service as assistant_service

    monkeypatch.setattr(
        assistant_service,
        "_classify_with_n_atlas",
        lambda message: "get_food_plan",
    )

    result = understand_message(
        "Help me feed my family on my income",
        "test-user",
    )

    assert result.intent == "get_food_plan"
    assert result.user_id == "test-user"

