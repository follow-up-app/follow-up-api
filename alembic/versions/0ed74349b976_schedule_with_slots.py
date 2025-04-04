"""schedule with slots

Revision ID: 0ed74349b976
Revises: 75ce17a5c82b
Create Date: 2025-03-30 18:39:13.427987

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '0ed74349b976'
down_revision = '75ce17a5c82b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('start_in', sa.DateTime(), nullable=False),
    sa.Column('repeat', sa.Enum('NO', 'WEEK', 'MOUTH', name='repeatenum'), nullable=True),
    sa.Column('period', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('schedules', sa.Column('week_days', sa.String(length=255), nullable=False))
    op.create_foreign_key(None, 'schedules', 'events', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_column('schedules', 'week_days')
    op.drop_table('events')
    # ### end Alembic commands ###
