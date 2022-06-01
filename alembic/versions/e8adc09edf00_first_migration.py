"""First migration

Revision ID: e8adc09edf00
Revises:
Create Date: 2022-06-01 14:27:36.329491

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


revision = 'e8adc09edf00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'charityproject',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.CheckConstraint(
            'full_amount > 0', name='full_amount_greater_than_zero'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'user',
        sa.Column(
            'id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=False
        ),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table(
        'donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.CheckConstraint('full_amount > 0', name='full_amount_greater_than_zero'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('donation')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('charityproject')
