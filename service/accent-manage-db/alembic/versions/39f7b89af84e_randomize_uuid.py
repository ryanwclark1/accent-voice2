"""randomize uuid

Revision ID: 39f7b89af84e
Revises: 3770e116222d

"""

# revision identifiers, used by Alembic.
revision = '39f7b89af84e'
down_revision = '3770e116222d'

import os

import sqlalchemy as sa

from alembic import op

infos_table = sa.sql.table('infos', sa.sql.column('uuid'))


def upgrade():
    new_uuid = os.environ['ACCENT_UUID']
    infos_query = infos_table.update().values({'uuid': new_uuid})
    op.get_bind().execute(infos_query)


def downgrade():
    pass
