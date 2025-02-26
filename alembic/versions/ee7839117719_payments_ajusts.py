"""payments ajusts

Revision ID: ee7839117719
Revises: 2a009cae236a
Create Date: 2024-09-20 02:23:15.161160

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ee7839117719'
down_revision = '2a009cae236a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('reference', sa.String(length=20), nullable=True))
    op.alter_column('payments', 'value',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'value',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.drop_column('payments', 'reference')
    # ### end Alembic commands ###
