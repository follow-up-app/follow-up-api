"""refresh tables -students - responsables

Revision ID: 61b85329975e
Revises: 57056d40a928
Create Date: 2023-08-13 21:28:11.341125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61b85329975e'
down_revision = '57056d40a928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract_responsibles', sa.Column('bond', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contract_responsibles', 'bond')
    # ### end Alembic commands ###
