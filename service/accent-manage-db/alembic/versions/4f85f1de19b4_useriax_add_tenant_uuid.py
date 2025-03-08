"""useriax_add_tenant_uuid

Revision ID: 4f85f1de19b4
Revises: 41b6afe5b164

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4f85f1de19b4'
down_revision = '41b6afe5b164'

TABLE = 'useriax'


def find_default_tenant_uuid():
    entity_table = sa.sql.table(
        'entity',
        sa.sql.column('id'),
        sa.sql.column('name'),
        sa.sql.column('tenant_uuid'),
    )
    query = sa.sql.select([entity_table.c.tenant_uuid]).order_by(entity_table.c.id)
    for row in op.get_bind().execute(query):
        return row.tenant_uuid


def associate_tenants():
    tbl = sa.sql.table('useriax', sa.sql.column('id'), sa.sql.column('tenant_uuid'))
    sql = "SELECT useriax.id, trunkfeatures.tenant_uuid FROM useriax, trunkfeatures WHERE trunkfeatures.protocol = 'iax' AND trunkfeatures.protocolid = useriax.id"
    useriax_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for useriax_id, tenant_uuid in useriax_to_tenant:
        query = tbl.update().where(tbl.c.id == useriax_id).values(tenant_uuid=tenant_uuid)
        op.execute(query)

    sql = "SELECT useriax.id, context.tenant_uuid FROM useriax JOIN context ON useriax.context = context.name LEFT JOIN trunkfeatures ON (trunkfeatures.protocol = 'iax' AND trunkfeatures.protocolid = useriax.id) WHERE trunkfeatures.protocolid IS NULL;"
    useriax_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for useriax_id, tenant_uuid in useriax_to_tenant:
        query = tbl.update().where(tbl.c.id == useriax_id).values(tenant_uuid=tenant_uuid)
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
