"""Pizza Type

Revision ID: 33f2e3a28d52
Revises: b2d216df60d7
Create Date: 2024-09-10 09:10:44.319459

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "33f2e3a28d52"
down_revision: Union[str, None] = "b2d216df60d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pizza_type",
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pizza_type_association",
        sa.Column("pizza_id", sa.UUID(), nullable=False),
        sa.Column("pizza_type_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pizza_id"],
            ["pizza.id"],
        ),
        sa.ForeignKeyConstraint(
            ["pizza_type_id"],
            ["pizza_type.id"],
        ),
        sa.PrimaryKeyConstraint("pizza_id", "pizza_type_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pizza_type_association")
    op.drop_table("pizza_type")
    # ### end Alembic commands ###