"""baseline do esquema existente

Revision ID: 0b0a446df992
Revises:
Create Date: 2026-09-16 15:41:47.432434

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "0b0a446df992"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
