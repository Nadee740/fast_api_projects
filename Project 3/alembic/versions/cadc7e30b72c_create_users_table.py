"""create users table

Revision ID: cadc7e30b72c
Revises: 
Create Date: 2023-11-10 17:47:27.089646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cadc7e30b72c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('email',sa.String(),nullable=False,unique=True),sa.Column('name',sa.String(),nullable=False),sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(),nullable=False,server_default=sa.text('now()')))
    #op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('email',sa.String(),nullable=False,unique=True))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
