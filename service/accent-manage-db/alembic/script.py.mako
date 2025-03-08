"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}

"""

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

<%
    kwargs = {}
    if config.cmd_opts.x:
        kwargs = dict(arg.split('=', 1) for arg in config.cmd_opts.x)
%>
def upgrade():
% if kwargs.get('accent_version'):
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='${kwargs['accent_version']}'))
% else:
    ${upgrades if upgrades else "pass"}
% endif


def downgrade():
    ${downgrades if downgrades else "pass"}
