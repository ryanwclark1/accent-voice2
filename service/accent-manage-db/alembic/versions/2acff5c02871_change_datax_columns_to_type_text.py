"""change dataX columns to type text

Revision ID: 2acff5c02871
Revises: 501dae22d6be

"""

# revision identifiers, used by Alembic.
revision = '2acff5c02871'
down_revision = '501dae22d6be'

from sqlalchemy.types import Text

from alembic import op


def upgrade():
    op.alter_column('queue_log', 'data1', type_=Text)
    op.alter_column('queue_log', 'data2', type_=Text)
    op.alter_column('queue_log', 'data3', type_=Text)
    op.alter_column('queue_log', 'data4', type_=Text)
    op.alter_column('queue_log', 'data5', type_=Text)
    op.alter_column('queue_log', 'data1', server_default='')
    op.alter_column('queue_log', 'data2', server_default='')
    op.alter_column('queue_log', 'data3', server_default='')
    op.alter_column('queue_log', 'data4', server_default='')
    op.alter_column('queue_log', 'data5', server_default='')


def downgrade():
    pass
