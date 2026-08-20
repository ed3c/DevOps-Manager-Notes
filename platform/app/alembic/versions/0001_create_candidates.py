"""create candidates table

Revision ID: 0001_candidates
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_candidates"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("git_commit", sa.String(length=40), nullable=False),
        sa.Column("model_version", sa.String(length=200), nullable=False),
        sa.Column("prompt_version", sa.String(length=200), nullable=False),
        sa.Column("config_version", sa.String(length=200), nullable=False),
        sa.Column("state", sa.String(length=40), nullable=False),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_candidates_git_commit", "candidates", ["git_commit"])
    op.create_index("ix_candidates_idempotency_key", "candidates", ["idempotency_key"])


def downgrade() -> None:
    op.drop_index("ix_candidates_idempotency_key", table_name="candidates")
    op.drop_index("ix_candidates_git_commit", table_name="candidates")
    op.drop_table("candidates")
