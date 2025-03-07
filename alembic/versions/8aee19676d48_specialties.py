"""specialties

Revision ID: 8aee19676d48
Revises: af6fe76699ee
Create Date: 2024-08-31 20:53:20.111981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '8aee19676d48'
down_revision = 'af6fe76699ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('specialties',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('value_hour', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('schedule_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('instructor_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('date_due', sa.Date(), nullable=False),
    sa.Column('date_scheduled', sa.Date(), nullable=True),
    sa.Column('date_done', sa.Date(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('status', sa.Enum('OPEN', 'SCHEDULED', 'DONE', name='paymentenum'), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'skills', type_='foreignkey')
    op.drop_column('skills', 'specialty_id')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_column('schedules', 'specialty_id')
    op.add_column('instructors', sa.Column('specialty_instructor_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('instructors', sa.Column('value_hour', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('instructors', sa.Column('value_mouth', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.create_foreign_key('instructors_specialty_instructor_id_fkey', 'instructors', 'specialties_instructor', ['specialty_instructor_id'], ['id'])
    op.create_table('specialties_instructor',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('company_id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('specialty', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='specialties_instructor_company_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='specialties_instructor_pkey')
    )
    op.drop_table('payments')
    op.drop_table('specialties')
    # ### end Alembic commands ###
