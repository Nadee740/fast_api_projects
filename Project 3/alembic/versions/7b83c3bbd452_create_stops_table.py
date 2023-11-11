"""create stops table

Revision ID: 7b83c3bbd452
Revises: cadc7e30b72c
Create Date: 2023-11-10 18:07:50.928297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b83c3bbd452'
down_revision: Union[str, None] = 'cadc7e30b72c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('stops',sa.Column('stop_id',sa.Integer(),primary_key=True),sa.Column('created_user_id',sa.Integer(),nullable=False),sa.ForeignKeyConstraint(['created_user_id'],['users.id'],ondelete='CASCADE',onupdate='CASCADE') ,sa.Column('stop_name',sa.String(),nullable=False,unique=True),sa.Column('is_active',sa.BOOLEAN,default=True,nullable=False),sa.Column('created_at',sa.TIMESTAMP(),nullable=False,server_default=sa.text('now()')))
    pass



def downgrade() -> None:
    op.drop_table('stops')
    pass
