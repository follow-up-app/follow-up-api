"""tables create - refresh

Revision ID: ae653dc6fdd5
Revises: d67a8bc60f5f
Create Date: 2023-06-07 22:01:30.044200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae653dc6fdd5'
down_revision = 'd67a8bc60f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructors', sa.Column('phone', sa.String(length=50), nullable=True))
    op.add_column('instructors', sa.Column('whats_app', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instructors', 'whats_app')
    op.drop_column('instructors', 'phone')
    # ### end Alembic commands ###
