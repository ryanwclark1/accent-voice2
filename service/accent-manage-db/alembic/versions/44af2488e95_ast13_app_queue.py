"""ast13: remove app_queue eventmemberstatus and eventwhencalled

Revision ID: 44af2488e95
Revises: 1a25b8b93e70

"""

# revision identifiers, used by Alembic.
revision = '44af2488e95'
down_revision = '1a25b8b93e70'

from sqlalchemy import sql
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer

from alembic import op

queue_table_old = sql.table('queue',
                            sql.column('eventmemberstatus'),
                            sql.column('eventwhencalled'))


def upgrade():
    _drop_queue_columns()


def _drop_queue_columns():
    op.drop_column('queue', 'eventmemberstatus')
    op.drop_column('queue', 'eventwhencalled')


def downgrade():
    _add_queue_columns()


def _add_queue_columns():
    op.add_column('queue',
                  Column('eventmemberstatus', Integer, nullable=False, server_default='0'))
    op.add_column('queue',
                  Column('eventwhencalled', Integer, nullable=False, server_default='0'))
    op.execute(queue_table_old
               .update()
               .values({'eventmemberstatus': 1, 'eventwhencalled': 1}))
