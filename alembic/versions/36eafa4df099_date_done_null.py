"""date done null

Revision ID: 36eafa4df099
Revises: cf2d123676e1
Create Date: 2024-09-08 23:31:34.065040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36eafa4df099'
down_revision = 'cf2d123676e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'date_done',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('payments', 'date_done',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
