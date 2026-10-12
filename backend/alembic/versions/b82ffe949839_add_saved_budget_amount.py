
"""add saved budget amount

Revision ID: b82ffe949839
Revises: 28ddbb62e59e
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b82ffe949839"
down_revision: Union[str, Sequence[str], None] = "28ddbb62e59e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the column as nullable so existing rows remain valid.
    op.add_column(
        "food_budgets",
        sa.Column(
            "budget_amount",
            sa.Numeric(12, 2),
            nullable=True,
        ),
    )

    # Preserve existing records by initializing the saved amount.
    op.execute(
        "UPDATE food_budgets "
        "SET budget_amount = recommended_amount "
        "WHERE budget_amount IS NULL"
    )

    # Require a value after all existing rows have been populated.
    op.alter_column(
        "food_budgets",
        "budget_amount",
        existing_type=sa.Numeric(12, 2),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("food_budgets", "budget_amount")
