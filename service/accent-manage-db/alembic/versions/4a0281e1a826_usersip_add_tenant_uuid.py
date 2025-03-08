"""usersip_add_tenant_uuid

Revision ID: 4a0281e1a826
Revises: 374507a67216

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4a0281e1a826'
down_revision = '374507a67216'


TABLE = 'usersip'


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
    tbl = sa.sql.table('usersip', sa.sql.column('id'), sa.sql.column('tenant_uuid'))
    sql = "SELECT usersip.id, context.tenant_uuid FROM usersip JOIN linefeatures ON (linefeatures.protocol = 'sip' AND linefeatures.protocolid = usersip.id) JOIN context ON linefeatures.context = context.name"
    usersip_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for usersip_id, tenant_uuid in usersip_to_tenant:
        query = tbl.update().where(tbl.c.id == usersip_id).values(tenant_uuid=tenant_uuid)
        op.execute(query)

    sql = "SELECT usersip.id, trunkfeatures.tenant_uuid FROM usersip, trunkfeatures WHERE trunkfeatures.protocol = 'sip' AND trunkfeatures.protocolid = usersip.id"
    usersip_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for usersip_id, tenant_uuid in usersip_to_tenant:
        query = tbl.update().where(tbl.c.id == usersip_id).values(tenant_uuid=tenant_uuid)
        op.execute(query)

    sql = "SELECT usersip.id, context.tenant_uuid FROM usersip JOIN context ON usersip.context = context.name LEFT JOIN linefeatures ON (linefeatures.protocol = 'sip' AND linefeatures.protocolid = usersip.id) LEFT JOIN trunkfeatures ON (trunkfeatures.protocol = 'sip' AND trunkfeatures.protocolid = usersip.id) WHERE linefeatures.protocolid IS NULL AND trunkfeatures.protocolid IS NULL;"
    usersip_to_tenant = op.get_bind().execute(sa.sql.text(sql))

    for usersip_id, tenant_uuid in usersip_to_tenant:
        query = tbl.update().where(tbl.c.id == usersip_id).values(tenant_uuid=tenant_uuid)
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
