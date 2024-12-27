"""empty message

Revision ID: b0044af96d65
Revises:
Create Date: 2024-12-26 20:13:54.437673

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b0044af96d65"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tg_user",
        sa.Column("tg_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("tg_id"),
        comment="User in Telegram",
    )
    op.create_table(
        "user_form",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_tg_id", sa.BIGINT(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("tag_or_number", sa.String(), nullable=False),
        sa.Column("region", sa.String(), nullable=False),
        sa.Column("notify", sa.Boolean(), nullable=False),
        sa.Column("meetings", sa.Boolean(), nullable=False),
        sa.Column("near_politic", sa.Boolean(), nullable=False),
        sa.Column("lpr_join", sa.Boolean(), nullable=False),
        sa.Column("other", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_tg_id"], ["tg_user.tg_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_form")
    op.drop_table("tg_user")
    # ### end Alembic commands ###
