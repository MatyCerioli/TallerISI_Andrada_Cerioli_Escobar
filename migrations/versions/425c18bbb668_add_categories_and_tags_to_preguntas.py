"""add categories and tags to preguntas

Revision ID: 425c18bbb668
Revises: d54634fa6bf4
Create Date: 2026-11-24

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '425c18bbb668'
down_revision = 'd54634fa6bf4'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Crear tabla categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

    # 2. Crear tabla tags
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

    # 3. Crear tabla asociativa question_tags
    op.create_table(
        'question_tags',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['preguntas.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id']),
        sa.PrimaryKeyConstraint('question_id', 'tag_id')
    )

    # 4. Modificar la tabla preguntas usando batch_alter_table (Requerido para SQLite)
    with op.batch_alter_table('preguntas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_preguntas_categories', 'categories', ['category_id'], ['id'])


def downgrade():
    with op.batch_alter_table('preguntas', schema=None) as batch_op:
        batch_op.drop_constraint('fk_preguntas_categories', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('question_tags')
    op.drop_table('tags')
    op.drop_table('categories')
