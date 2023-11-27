"""create user table

Revision ID: 92c9796ad834
Revises:
Create Date: 2023-11-26 21:14:25.198983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '92c9796ad834'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String()),
        sa.Column('password', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
    )

    # Create the task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, autoincrement=True),
        sa.Column('title', sa.String(), index=True, nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('done', sa.Boolean(), default=False),
        sa.Column('order', sa.Integer(), index=True, default=0),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('user.id')),
    )

    # Create the shared_task table
    op.create_table(
        'shared_task',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.Column('shared_with_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
    )

def downgrade():
    # Drop the shared_task table
    op.drop_table('shared_task')

    # Drop the task table
    op.drop_table('task')

    # Drop the user table
    op.drop_table('user')
