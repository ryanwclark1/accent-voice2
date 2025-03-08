"""add web service UUID

Revision ID: 30d7dcbb9133
Revises: 53fbfa53b47c

"""

# revision identifiers, used by Alembic.
revision = '30d7dcbb9133'
down_revision = '53fbfa53b47c'

import sqlalchemy as sa

from alembic import op

table_name = 'accesswebservice'
column_name = 'uuid'
constraint_name = '{}_{}_key'.format(table_name, column_name)


def upgrade():
    op.add_column(
        table_name,
        sa.Column(
            column_name,
            sa.String(38),
            nullable=False,
            server_default=sa.text('uuid_generate_v4()')))
    op.create_unique_constraint(constraint_name, table_name, [column_name])


def downgrade():
    op.drop_constraint(constraint_name, table_name)
    op.drop_column(table_name, column_name)
