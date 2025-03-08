"""call_filter_add_tenant_uuid

Revision ID: 21f6963c1d35
Revises: 4f86216ba603

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '21f6963c1d35'
down_revision = '4f86216ba603'

TABLE = 'callfilter'


def find_default_tenant_uuid():
    entity_table = sa.sql.table(
        'entity',
        sa.sql.column('id'),
        sa.sql.column('tenant_uuid'),
    )
    query = sa.sql.select([entity_table.c.tenant_uuid]).order_by(entity_table.c.id)
    for row in op.get_bind().execute(query):
        return row.tenant_uuid


def associate_tenants():
    tbl = sa.sql.table('callfilter', sa.sql.column('id'), sa.sql.column('tenant_uuid'))
    sql = "SELECT callfilter.id, entity.tenant_uuid FROM callfilter, entity WHERE entity.id=callfilter.entity_id"
    callfilter_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for callfilter_id, tenant_uuid in callfilter_to_tenant:
        query = tbl.update().where(tbl.c.id == callfilter_id).values(tenant_uuid=tenant_uuid)
        op.execute(query)


def upgrade():
    default_tenant = find_default_tenant_uuid()
    op.add_column(
        TABLE,
        sa.Column(
            'tenant_uuid',
            sa.String(36),
            sa.ForeignKey('tenant.uuid', ondelete='CASCADE'),
            nullable=False,
            server_default=default_tenant),
    )
    associate_tenants()
    op.alter_column(TABLE, 'tenant_uuid', server_default=None)


def downgrade():
    op.drop_column(TABLE, 'tenant_uuid')
