"""specialties foreikey

Revision ID: cf2d123676e1
Revises: 8aee19676d48
Create Date: 2024-08-31 22:15:16.158366

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils



# revision identifiers, used by Alembic.
revision = 'cf2d123676e1'
down_revision = '8aee19676d48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('specialties_instructor')
    op.drop_constraint('instructors_specialty_instructor_id_fkey', 'instructors', type_='foreignkey')
    op.drop_column('instructors', 'specialty_instructor_id')
    op.drop_column('instructors', 'value_mouth')
    op.drop_column('instructors', 'value_hour')
    op.add_column('schedules', sa.Column('specialty_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True))
    op.create_foreign_key(None, 'schedules', 'specialties', ['specialty_id'], ['id'])
    op.add_column('skills', sa.Column('specialty_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True))
    op.create_foreign_key(None, 'skills', 'specialties', ['specialty_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'skills', type_='foreignkey')
    op.drop_column('skills', 'specialty_id')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_column('schedules', 'specialty_id')
    op.add_column('instructors', sa.Column('value_hour', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('instructors', sa.Column('value_mouth', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('instructors', sa.Column('specialty_instructor_id', postgresql.UUID(), autoincrement=False, nullable=True))
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
    # ### end Alembic commands ###
