from typing import Literal
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    income_amount: Decimal = Field(gt=0)
    income_frequency: str
    household_size: int = Field(gt=0)
    location: str
    preferred_language: str = "en"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: EmailStr
    income_amount: Decimal
    income_frequency: str
    household_size: int
    location: str
    preferred_language: str


class FoodBudgetCreate(BaseModel):
    user_id: str



class FoodBudgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    income_amount: Decimal
    recommended_amount: Decimal
    budget_amount: Decimal
    period: str


class FoodBudgetUpdate(BaseModel):
    budget_amount: Decimal = Field(ge=0)


class SavingsGoalCreate(BaseModel):
    user_id: str
    name: str = Field(min_length=2, max_length=100)
    target_amount: Decimal = Field(gt=0)
    duration_months: int = Field(gt=0)
    contribution_frequency: Literal["daily", "weekly", "monthly"] = "monthly"


class SavingsGoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    name: str
    target_amount: Decimal
    current_amount: Decimal
    duration_months: int
    contribution_frequency: str
    contribution_amount: Decimal
    status: str


class SavingsProgressResponse(BaseModel):
    goal_id: str
    goal_name: str
    target_amount: Decimal
    current_amount: Decimal
    remaining_amount: Decimal
    progress_percentage: Decimal
    status: str


class SavingsContributionCreate(BaseModel):
    amount: Decimal = Field(gt=0)


class SavingsContributionResponse(BaseModel):
    goal_id: str
    goal_name: str
    contribution_amount: Decimal
    current_amount: Decimal
    target_amount: Decimal
    remaining_amount: Decimal
    progress_percentage: Decimal
    status: str



class FoodPackageItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: Decimal = Field(gt=0)
    unit: str = Field(min_length=1, max_length=30)
    estimated_unit_price: Decimal | None = Field(
        default=None,
        ge=0,
    )



class FoodPackageItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    quantity: Decimal
    unit: str
    estimated_unit_price: Decimal | None
    price_checked_at: datetime | None
    verification_status: str



class FoodPackageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str
    package_type: str
    estimated_cost: Decimal
    household_size: int
    duration_days: int
    items: list[FoodPackageItemResponse] = Field(default_factory=list)
    contents_status: Literal[
        "not_defined",
        "partially_verified",
        "verified",
    ] = "not_defined"


class FoodRecommendationResponse(BaseModel):
    user_id: str
    recommended_package: FoodPackageResponse
    reason: str


class FoodPlanRequest(BaseModel):
    user_id: str


class FoodPlanResponse(BaseModel):
    user_id: str
    income_amount: Decimal
    household_size: int
    recommended_food_budget: Decimal
    recommended_package: FoodPackageResponse
    reason: str



class FoodAssistantRequest(BaseModel):
    user_id: str
    message: str = Field(min_length=1, max_length=2000)
    language: Literal["en", "yo", "ig", "ha", "en-ng"] = "en"




class FoodAssistantIntent(BaseModel):
    intent: Literal[
        "get_food_plan",
        "adjust_food_budget",
        "show_food_plan",
    ]
    user_id: str
    budget_amount: Decimal | None = None
    income_amount: Decimal | None = Field(default=None, gt=0)
    household_size: int | None = Field(default=None, gt=0)



class FoodAssistantChatResponse(BaseModel):
    message: str
    food_plan: FoodPlanResponse


