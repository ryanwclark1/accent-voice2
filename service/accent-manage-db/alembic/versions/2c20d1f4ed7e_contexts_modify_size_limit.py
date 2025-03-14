"""contexts modify size limit to 79 chars

Revision ID: 2c20d1f4ed7e
Revises: 1c175d6b47c7

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2c20d1f4ed7e'
down_revision = '1c175d6b47c7'

TBL_CONTEXT = 'context'
TBL_CONTEXTINCLUDE = 'contextinclude'

tables = (
    'agent_login_status',
    'agentfeatures',
    'contextinclude',
    'contextmember',
    'contextnumbers',
    'extensions',
    'linefeatures',
    'outcall',
    'queuefeatures',
    'queue',
    'sccpline',
    'trunkfeatures',
    'usercustom',
    'voicemail',
    'useriax',
)

tables_preprocess = (
    'agentfeatures',
    'conference',
    'groupfeatures',
    'incall',
    'outcall',
    'queuefeatures',
    'userfeatures',
)


def upgrade():
    op.alter_column(TBL_CONTEXT, 'name', type_=sa.String(length=79))
    op.alter_column(TBL_CONTEXTINCLUDE, 'include', type_=sa.String(length=79))

    for table in tables:
        op.alter_column(table, 'context', type_=sa.String(length=79))

    for table in tables_preprocess:
        op.alter_column(table, 'preprocess_subroutine', type_=sa.String(length=79))


def downgrade():
    op.alter_column(TBL_CONTEXT, 'name', type_=sa.String(length=39))
    op.alter_column(TBL_CONTEXTINCLUDE, 'include', type_=sa.String(length=39))

    for table in tables:
        new_length = 39
        if table == 'sccpline':
            new_length = 80
        if table == 'agentfeatures':
            new_length = 40
        op.alter_column(table, 'context', type_=sa.String(length=new_length))

    for table in tables_preprocess:
        op.alter_column(table, 'preprocess_subroutine', type_=sa.String(length=39))
