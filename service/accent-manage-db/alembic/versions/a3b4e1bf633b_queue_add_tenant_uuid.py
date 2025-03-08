"""queue add tenant_uuid

Revision ID: a3b4e1bf633b
Revises: 12f9880ae872

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a3b4e1bf633b'
down_revision = '12f9880ae872'


TABLE = 'queuefeatures'


def get_context_tenant_map():
    tbl = sa.sql.table('context', sa.sql.column('name'), sa.sql.column('tenant_uuid'))
    query = sa.sql.select([tbl.c.name, tbl.c.tenant_uuid])
    rows = op.get_bind().execute(query)
    return {row.name: row.tenant_uuid for row in rows}


def associate_tenants():
    tbl = sa.sql.table(TABLE, sa.sql.column('context'), sa.sql.column('tenant_uuid'))

    for name, uuid in get_context_tenant_map().items():
        query = tbl.update().where(tbl.c.context == name).values(tenant_uuid=uuid)
        op.execute(query)


def remove_no_tenants():
    tbl = sa.sql.table(TABLE, sa.sql.column('tenant_uuid'))
    query = tbl.delete().where(tbl.c.tenant_uuid == None)
    op.execute(query)


def upgrade():
    op.add_column(
        TABLE,
        sa.Column(
            'tenant_uuid',
            sa.String(36),
            sa.ForeignKey('tenant.uuid', ondelete='CASCADE'),
            nullable=True),
    )
    associate_tenants()
    remove_no_tenants()
    op.alter_column(TABLE, 'tenant_uuid', nullable=False)


def downgrade():
    op.drop_column(TABLE, 'tenant_uuid')
