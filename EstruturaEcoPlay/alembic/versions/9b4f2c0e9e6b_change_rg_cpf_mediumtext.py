"""change rg/cpf columns to MEDIUMTEXT

Revision ID: 9b4f2c0e9e6b
Revises: 5f1ce3c77a5a
Create Date: 2025-12-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9b4f2c0e9e6b'
down_revision = '5f1ce3c77a5a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change rg_path and cpf_path to MEDIUMTEXT to allow storing base64 payloads
    op.alter_column('usuarios', 'rg_path', existing_type=sa.String(length=255), type_=mysql.MEDIUMTEXT(), existing_nullable=False, nullable=True)
    op.alter_column('usuarios', 'cpf_path', existing_type=sa.String(length=255), type_=mysql.MEDIUMTEXT(), existing_nullable=False, nullable=True)


def downgrade() -> None:
    # Revert back to VARCHAR(255)
    op.alter_column('usuarios', 'rg_path', existing_type=mysql.MEDIUMTEXT(), type_=sa.String(length=255), existing_nullable=True, nullable=False)
    op.alter_column('usuarios', 'cpf_path', existing_type=mysql.MEDIUMTEXT(), type_=sa.String(length=255), existing_nullable=True, nullable=False)
