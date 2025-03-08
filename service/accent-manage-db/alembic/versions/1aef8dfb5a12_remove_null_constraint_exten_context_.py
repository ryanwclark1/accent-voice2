"""remove_null_constraint_exten_context_from_incall

Revision ID: 1aef8dfb5a12
Revises: 549c621ae619

"""

# revision identifiers, used by Alembic.
revision = '1aef8dfb5a12'
down_revision = '549c621ae619'

from alembic import op


def upgrade():
    op.alter_column('incall', 'exten', nullable=True)
    op.alter_column('incall', 'context', nullable=True)
    op.alter_column('incall', 'description', nullable=True)


def downgrade():
    op.alter_column('incall', 'exten', nullable=False)
    op.alter_column('incall', 'context', nullable=False)
    op.alter_column('incall', 'description', nullable=False)
