"""create procedure schedule

Revision ID: f028e581b7e3
Revises: adb8f52d441c
Create Date: 2024-06-28 00:44:15.367347

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f028e581b7e3'
down_revision = 'adb8f52d441c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('procedures_schedueles',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('schedule_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('student_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('skill_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('tries', sa.Integer(), nullable=False),
    sa.Column('goal', sa.Float(), nullable=False),
    sa.Column('period', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('objective', sa.String(length=1000), nullable=True),
    sa.Column('stimulus', sa.String(length=1000), nullable=True),
    sa.Column('answer', sa.String(length=1000), nullable=True),
    sa.Column('consequence', sa.String(length=1000), nullable=True),
    sa.Column('materials', sa.String(length=1000), nullable=True),
    sa.Column('help', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('executions', sa.Column('procedure_schedule_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False))
    op.alter_column('executions', 'procedure_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.create_foreign_key(None, 'executions', 'procedures', ['procedure_schedule_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'executions', type_='foreignkey')
    op.alter_column('executions', 'procedure_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('executions', 'procedure_schedule_id')
    op.drop_table('procedures_schedueles')
    # ### end Alembic commands ###
