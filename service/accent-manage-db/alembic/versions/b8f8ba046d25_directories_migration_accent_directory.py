"""directories: migration accent directory

Revision ID: b8f8ba046d25
Revises: c22356e22a13

"""

# revision identifiers, used by Alembic.
revision = 'b8f8ba046d25'
down_revision = 'c22356e22a13'

from sqlalchemy import and_, sql

from alembic import op

directories = sql.table(
    'directories',
    sql.column('id'),
    sql.column('name'),
    sql.column('uri'),
    sql.column('dirtype'),
    sql.column('description'),
    sql.column('accent_username'),
    sql.column('accent_password'),
    sql.column('accent_verify_certificate'),
    sql.column('accent_custom_ca_path'),
    sql.column('auth_backend'),
    sql.column('auth_host'),
    sql.column('auth_port'),
    sql.column('auth_verify_certificate'),
    sql.column('auth_custom_ca_path'),
)
webservice = sql.table(
    'accesswebservice',
    sql.column('login'),
    sql.column('passwd'),
)
old_uri = 'http://localhost:9487'
new_uri = 'https://localhost:9486'
username = 'accent-dird-accent-backend'
default_ca_path = '/usr/share/accent-certs/server.crt'
dirtype = 'accent'

def find_ws_password(conn, username):
    password = None
    query = sql.select([webservice.c.passwd]).where(webservice.c.login == username)
    for row in conn.execute(query):
        password = row.passwd

    if not password:
        raise Exception('failed to find a password for user {}'.format(username))

    return password


def upgrade():
    password = find_ws_password(op.get_bind(), username)
    op.execute(directories.update().values(
        uri=new_uri,
        accent_username=username,
        accent_password=password,
        accent_verify_certificate=True,
        accent_custom_ca_path=default_ca_path,
        auth_backend='accent_service',
        auth_host='localhost',
        auth_port=9497,
        auth_verify_certificate=True,
        auth_custom_ca_path=default_ca_path,
    ).where(and_(directories.c.dirtype == dirtype, directories.c.uri == old_uri)))


def downgrade():
    op.execute(directories.update().values(
        uri=old_uri,
        accent_username=None,
        accent_password=None,
        accent_verify_certificate=False,
        accent_custom_ca_path=None,
        auth_backend=None,
        auth_host=None,
        auth_port=None,
        auth_verify_certificate=False,
        auth_custom_ca_path=None,
    ).where(and_(directories.c.dirtype == dirtype, directories.c.uri == new_uri)))
