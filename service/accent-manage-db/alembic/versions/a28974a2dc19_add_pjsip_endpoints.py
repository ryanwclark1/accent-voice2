"""add pjsip endpoints

Revision ID: a28974a2dc19
Revises: 4aa03039dd2e

"""

from sqlalchemy import Boolean, Column, Enum, Integer, String, Text, text
from sqlalchemy import ForeignKey as FK
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a28974a2dc19'
down_revision = '4aa03039dd2e'

UUID_GEN = 'uuid_generate_v4()'

endpoint_sip_section_type = Enum(
    'aor',
    'auth',
    'endpoint',
    'identify',
    'outbound_auth',
    'registration_outbound_auth',
    'registration',
    name='endpoint_sip_section_type',
)


def upgrade():
    op.create_table(
        'endpoint_sip',
        Column('uuid', UUID, server_default=text(UUID_GEN), primary_key=True),
        Column('label', Text),
        Column('name', Text, nullable=False, unique=True),
        Column('asterisk_id', Text),
        Column('tenant_uuid', String(36), FK('tenant.uuid', ondelete='CASCADE'), nullable=False),
        Column('transport_uuid', UUID, FK('pjsip_transport.uuid')),
        Column('context_id', Integer, FK('context.id')),
        Column('template', Boolean, server_default=text('false')),
    )
    op.create_table(
        'endpoint_sip_section',
        Column('uuid', UUID, server_default=text(UUID_GEN), primary_key=True),
        Column('endpoint_sip_uuid', UUID, FK('endpoint_sip.uuid', ondelete='CASCADE'), nullable=False),
        Column('type', endpoint_sip_section_type, nullable=False)
    )
    op.create_unique_constraint(
        'endpoint_sip_section_type_endpoint_sip_uuid_key',
        'endpoint_sip_section',
        ['type', 'endpoint_sip_uuid'],
    )
    op.create_table(
        'endpoint_sip_section_option',
        Column('uuid', UUID, server_default=text(UUID_GEN), primary_key=True),
        Column('key', Text, nullable=False),
        Column('value', Text, nullable=False),
        Column(
            'endpoint_sip_section_uuid',
            UUID,
            FK('endpoint_sip_section.uuid', ondelete='CASCADE'),
            nullable=False
        ),
    )
    op.create_table(
        'endpoint_sip_template',
        Column('child_uuid', UUID, FK('endpoint_sip.uuid', ondelete='CASCADE'), primary_key=True),
        Column('parent_uuid', UUID, FK('endpoint_sip.uuid', ondelete='CASCADE'), primary_key=True),
    )
    op.add_column(
        'linefeatures',
        Column('endpoint_sip_uuid', UUID, FK('endpoint_sip.uuid', ondelete='SET NULL')),
    )
    op.add_column(
        'trunkfeatures',
        Column('endpoint_sip_uuid', UUID, FK('endpoint_sip.uuid', ondelete='SET NULL')),
    )


def downgrade():
    op.drop_column('trunkfeatures', 'endpoint_sip_uuid')
    op.drop_column('linefeatures', 'endpoint_sip_uuid')
    op.drop_table('endpoint_sip_template')
    op.drop_table('endpoint_sip_section_option')
    op.drop_table('endpoint_sip_section')
    op.drop_table('endpoint_sip')
    endpoint_sip_section_type.drop(op.get_bind())
