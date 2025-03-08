"""remove_loginclient_passwdclient_data_from_userfeatures

Revision ID: 404300b7c16d
Revises: eee032b308b

"""

from sqlalchemy import sql

from alembic import op

# revision identifiers, used by Alembic.
revision = '404300b7c16d'
down_revision = 'eee032b308b'

userfeatures = sql.table(
    'userfeatures',
    sql.column('loginclient'),
    sql.column('passwdclient'),
)


def upgrade():
    op.execute(userfeatures.update().values(loginclient='', passwdclient=''))


def downgrade():
    pass
