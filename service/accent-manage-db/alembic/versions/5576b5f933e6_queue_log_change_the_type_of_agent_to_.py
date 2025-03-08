"""queue_log: change the type of agent to text

Revision ID: 5576b5f933e6
Revises: 28721fe085d3

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5576b5f933e6'
down_revision = '28721fe085d3'


def upgrade():
    op.alter_column('queue_log', 'agent', nullable=False, server_default='', type_=sa.Text)


def downgrade():
    op.alter_column('queue_log', 'agent', nullable=False, server_default='', type_=sa.String(50))
