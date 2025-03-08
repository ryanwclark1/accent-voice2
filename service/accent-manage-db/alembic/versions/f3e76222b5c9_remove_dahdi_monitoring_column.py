"""remove-dahdi-monitoring-column

Revision ID: f3e76222b5c9
Revises: 0269f5e35792

"""

from sqlalchemy import Column, String

from alembic import op

# revision identifiers, used by Alembic.
revision = 'f3e76222b5c9'
down_revision = '0269f5e35792'


def upgrade():
    op.drop_column('monitoring', 'dahdi_monitor_ports')


def downgrade():
    op.add_column('monitoring', Column('dahdi_monitor_ports', String(255)))
