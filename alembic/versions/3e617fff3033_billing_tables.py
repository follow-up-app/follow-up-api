"""billing tables

Revision ID: 3e617fff3033
Revises: 459919936310
Create Date: 2024-10-13 20:10:49.721401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils
# revision identifiers, used by Alembic.
revision = '3e617fff3033'
down_revision = '459919936310'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoices',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plans',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('social_name', sa.String(length=100), nullable=True),
    sa.Column('fantasy_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_doctors',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_medicines',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('medicine', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.String(length=50), nullable=False),
    sa.Column('measure', sa.String(length=50), nullable=True),
    sa.Column('schedules', sa.String(length=50), nullable=True),
    sa.Column('anotations', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_plans',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('plan_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', name='statusenum'), nullable=False),
    sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bilings',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('company_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('schedule_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('reference', sa.String(length=20), nullable=True),
    sa.Column('category', sa.Enum('PERSONAL', 'PLAN', name='categoryenum'), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('date_due', sa.Date(), nullable=False),
    sa.Column('date_done', sa.Date(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('status', sa.Enum('OPEN', 'CONFIRMED', 'GENERATE_INVOICE', 'DONE', name='billingenum'), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoices_billings',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('invoice_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('billing_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['billing_id'], ['bilings.id'], ),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('specialties_instructor')
    op.add_column('contractors', sa.Column('mode_billing', sa.Enum('OPEN', 'CONFIRMED', 'DONE', name='billingenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contractors', 'mode_billing')
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
    op.drop_table('invoices_billings')
    op.drop_table('bilings')
    op.drop_table('student_plans')
    op.drop_table('student_medicines')
    op.drop_table('student_doctors')
    op.drop_table('plans')
    op.drop_table('invoices')
    # ### end Alembic commands ###
