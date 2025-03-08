# accent_auth/bootstrap.py

# Copyright 2023 Accent Communications

import logging
import os
import random
import string
import sys
import tempfile
import traceback
from typing import TYPE_CHECKING

# from accent.config_helper import parse_config_file, read_config_file_hierarchy  # REMOVED

from accent_auth.db import DAO
from accent_auth.services.policy import PolicyService
from accent_auth.services.user import UserService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# Use settings from config files
from accent_auth.config.app import settings as app_settings
from accent_auth.config.db import settings as db_settings

DEFAULT_ACCENT_AUTH_CONFIG_FILE = "/etc/accent-auth/config.yml"  # Still used?

CLI_CONFIG_DIR = "/root/.config/accent-auth-cli"  # Keep
CLI_CONFIG_FILENAME = os.path.join(CLI_CONFIG_DIR, "050-credentials.yml")  # Keep
CLI_CONFIG = """\
auth:
  username: {}
  password: {}
  backend: accent_user
"""  # Keep

VALID_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
USERNAME = "accent-auth-cli"
PURPOSE = "internal"
DEFAULT_POLICY_SLUG = "accent_default_master_user_policy"
AUTHENTICATION_METHOD = "native"

ERROR_MSG = """\
Failed to bootstrap accent-auth. Error is logged at {log_file}.
"""

logger = logging.getLogger(__name__)


def save_exception_and_exit():
    with tempfile.NamedTemporaryFile(
        mode="w", prefix="accent-auth-bootstrap-", delete=False
    ) as log_file:
        traceback.print_exc(file=log_file)
        print(ERROR_MSG.format(log_file=log_file.name), file=sys.stderr)
    sys.exit(1)


async def create_initial_user(
    db_uri: str,  # Keep, but it's not actually *used* inside this function anymore
    username: str,
    password: str,
    purpose: str,
    authentication_method: str,
    policy_slug: str,
    session: AsyncSession,  # Add session as an argument
) -> None:
    """Creates the initial user if it doesn't already exist. This is now async."""

    dao = DAO.from_defaults()  # Use the DAO
    policy_service = PolicyService(dao)
    user_service = UserService(dao)

    # ALL database interactions must now be async.
    if await user_service.get_user_by_login(login=username, db=session):
        # Already bootstrapped, just skip
        return

    user = await user_service.create(
        db=session,
        enabled=True,
        username=username,
        password=password,  # UserService now handles hashing
        purpose=purpose,
        authentication_method=authentication_method,
        tenant_uuid=await dao.tenant.find_top_tenant(
            session=session
        ),  # Find top tenant
        email_address="dummy@email.com",  # Added, since this is required now.
    )
    policy = await policy_service.find_by(
        slug=policy_slug, session=session
    )  # Get the policy
    if not policy:
        raise Exception(f"Policy with slug '{policy_slug}' not found.")

    await user_service.add_policy(
        user["uuid"], policy.uuid, db=session
    )  # Associate the user with the policy.

    # await session.commit()  # REMOVED: Session management is handled by the lifespan event.


def write_private_file(filename, username, content):
    try:
        # Use getpwnam from pwd module
        import pwd

        user = pwd.getpwnam(username)
        uid = user.pw_uid
        gid = user.pw_gid

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Create/overwrite the file
        with open(filename, "w") as f:
            f.write(content)

        # Set ownership and permissions
        os.chown(filename, uid, gid)
        os.chmod(filename, 0o600)  # Set permissions to read/write for owner only

    except KeyError:
        raise Exception(f"Unknown user {username}")
    except Exception as e:
        raise Exception(f"Failed to write private file: {e}")


def random_string(length):
    return "".join(random.SystemRandom().choice(VALID_CHARS) for _ in range(length))
