"""add procedure id in procedure schedule

Revision ID: a8c4dfed1d43
Revises: f028e581b7e3
Create Date: 2024-07-07 20:53:51.076701

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'a8c4dfed1d43'
down_revision = 'f028e581b7e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('procedures_schedueles', sa.Column('procedure_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False))
    op.create_foreign_key(None, 'procedures_schedueles', 'procedures', ['procedure_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'procedures_schedueles', type_='foreignkey')
    op.drop_column('procedures_schedueles', 'procedure_id')
    # ### end Alembic commands ###
