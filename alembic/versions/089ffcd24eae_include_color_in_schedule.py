"""include color in schedule

Revision ID: 089ffcd24eae
Revises: 91460b2608c6
Create Date: 2024-01-04 00:02:19.926748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '089ffcd24eae'
down_revision = '91460b2608c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedules', sa.Column('color', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'color')
    # ### end Alembic commands ###
