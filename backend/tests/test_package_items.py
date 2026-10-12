from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import FoodPackage, FoodPackageItem


@pytest.fixture
def package_api():
    # Create an isolated, in-memory SQLite database.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create only the tables needed for this test.
    FoodPackage.__table__.create(bind=test_engine)
    FoodPackageItem.__table__.create(bind=test_engine)

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    # Override the normal database dependency.
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create a package in the isolated test database.
    with TestingSessionLocal() as db:
        package = FoodPackage(
            name="Test Food Plan",
            description="Temporary package for automated testing.",
            package_type="basic",
            estimated_cost=Decimal("25000.00"),
            household_size=1,
            duration_days=30,
        )

        db.add(package)
        db.commit()
        db.refresh(package)

        package_id = package.id

    # Do not use a context manager here: we do not want
    # the application's startup seeding function to run.
    client = TestClient(app)

    yield client, package_id

    app.dependency_overrides.pop(get_db, None)
    test_engine.dispose()


def test_add_food_package_item(package_api):
    client, package_id = package_api

    response = client.post(
        f"/packages/{package_id}/items",
        json={
            "name": "Test Rice",
            "quantity": 5,
            "unit": "kg",
            "estimated_unit_price": 1200,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == package_id
    assert data["name"] == "Test Food Plan"
    assert Decimal(data["estimated_cost"]) == Decimal("25000.00")

    assert len(data["items"]) == 1

    item = data["items"][0]

    assert item["name"] == "Test Rice"
    assert Decimal(item["quantity"]) == Decimal("5")
    assert item["unit"] == "kg"
    assert item["verification_status"] == "unverified"

    assert data["contents_status"] == "partially_verified"
    