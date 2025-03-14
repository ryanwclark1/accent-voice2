"""add a meeting number

Revision ID: b7d3c4701095
Revises: 2b51ff81d388

"""

import random

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b7d3c4701095'
down_revision = '2b51ff81d388'

TABLE_NAME = 'meeting'
COLUMN_NAME = 'number'


meeting_tbl = sa.sql.table(
    TABLE_NAME,
    sa.column('uuid'),
    sa.column('number'),
)

def random_number(length=6):
    return str(random.randint(0, int('9' * length))).rjust(length, '0')


def upgrade():
    op.add_column(TABLE_NAME, sa.Column(COLUMN_NAME, sa.Text))

    query = sa.sql.select([meeting_tbl.c.uuid])
    for row in op.get_bind().execute(query):
        op.execute(
            meeting_tbl.update().where(meeting_tbl.c.uuid==row.uuid).values(number=random_number())
        )

    op.alter_column(TABLE_NAME, COLUMN_NAME, nullable=False)


def downgrade():
    op.drop_column(TABLE_NAME, COLUMN_NAME)
