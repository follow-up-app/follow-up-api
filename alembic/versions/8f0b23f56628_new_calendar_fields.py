"""new calendar fields

Revision ID: 8f0b23f56628
Revises: 089ffcd24eae
Create Date: 2024-01-17 01:09:39.527316

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '8f0b23f56628'
down_revision = '089ffcd24eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    eventrepeat = postgresql.ENUM('NO', 'WEEK', 'MOUTH', name='eventrepeat')
    eventrepeat.create(op.get_bind())
    
    op.add_column('schedules', sa.Column('start_hour', sa.String(length=20), nullable=True))
    op.add_column('schedules', sa.Column('end_hour', sa.String(length=20), nullable=True))
    op.add_column('schedules', sa.Column('repeat', sa.Enum('NO', 'WEEK', 'MOUTH', name='eventrepeat'), nullable=True))
    op.add_column('schedules', sa.Column('period', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'period')
    op.drop_column('schedules', 'repeat')
    op.drop_column('schedules', 'end_hour')
    op.drop_column('schedules', 'start_hour')
    # ### end Alembic commands ###
