from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    income_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    income_frequency: Mapped[str] = mapped_column(String(20))
    household_size: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String(100))
    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    budgets: Mapped[list["FoodBudget"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    savings_goals: Mapped[list["SavingsGoal"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class FoodBudget(Base):
    __tablename__ = "food_budgets"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    income_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    recommended_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    period: Mapped[str] = mapped_column(
        String(20),
        default="monthly",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="budgets"
    )


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100))
    target_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    current_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    duration_months: Mapped[int] = mapped_column(Integer)

    contribution_frequency: Mapped[str] = mapped_column(
        String(20)
    )

    contribution_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="savings_goals"
    )


class FoodPackage(Base):
    __tablename__ = "food_packages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[str] = mapped_column(
        String(255)
    )

    package_type: Mapped[str] = mapped_column(
        String(30)
    )

    estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    household_size: Mapped[int] = mapped_column(
        Integer
    )

    duration_days: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
















