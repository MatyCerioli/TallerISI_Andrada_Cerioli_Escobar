"""add agente_ia table

Revision ID: 5db09f6b0d19
Revises: 425c18bbb668
Create Date: 2026-11-24

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5db09f6b0d19'
down_revision = '425c18bbb668'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Crear la tabla agentes_ia (hereda de autores)
    op.create_table(
        'agentes_ia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('modelo', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['autores.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Alterar columna nombre en autores usando modo batch (Requerido para SQLite)
    with op.batch_alter_table('autores', schema=None) as batch_op:
        batch_op.alter_column(
            'nombre',
            existing_type=sa.VARCHAR(length=120),
            type_=sa.String(length=100),
            existing_nullable=False
        )


def downgrade():
    with op.batch_alter_table('autores', schema=None) as batch_op:
        batch_op.alter_column(
            'nombre',
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=120),
            existing_nullable=False
        )

    op.drop_table('agentes_ia')
