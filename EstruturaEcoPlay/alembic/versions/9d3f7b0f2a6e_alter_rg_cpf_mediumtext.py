"""Alter rg/cpf to MEDIUMTEXT

Revision ID: 9d3f7b0f2a6e
Revises: 5f1ce3c77a5a
Create Date: 2025-12-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '9d3f7b0f2a6e'
down_revision: Union[str, Sequence[str], None] = '5f1ce3c77a5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Alter rg_path and cpf_path to MEDIUMTEXT to allow base64 image strings
    op.alter_column('usuarios', 'rg_path', existing_type=sa.String(length=255), type_=mysql.MEDIUMTEXT(), existing_nullable=True)
    op.alter_column('usuarios', 'cpf_path', existing_type=sa.String(length=255), type_=mysql.MEDIUMTEXT(), existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to String(255)
    op.alter_column('usuarios', 'rg_path', existing_type=mysql.MEDIUMTEXT(), type_=sa.String(length=255), existing_nullable=True)
    op.alter_column('usuarios', 'cpf_path', existing_type=mysql.MEDIUMTEXT(), type_=sa.String(length=255), existing_nullable=True)
