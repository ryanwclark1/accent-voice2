# Copyright 2023 Accent Communications

import argparse
import os
import random
import string
import sys
import tempfile
import traceback
from pwd import getpwnam

from accent.config_helper import parse_config_file, read_config_file_hierarchy

from accent_auth import services
from accent_auth.database import queries
from accent_auth.database.helpers import commit_or_rollback, init_db

DEFAULT_ACCENT_AUTH_CONFIG_FILE = '/etc/accent-auth/config.yml'

CLI_CONFIG_DIR = '/root/.config/accent-auth-cli'
CLI_CONFIG_FILENAME = os.path.join(CLI_CONFIG_DIR, '050-credentials.yml')
CLI_CONFIG = '''\
auth:
  username: {}
  password: {}
  backend: accent_user
'''

VALID_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
USER = 'accent-auth'
USERNAME = 'accent-auth-cli'
PURPOSE = 'internal'
DEFAULT_POLICY_SLUG = 'accent_default_master_user_policy'
AUTHENTICATION_METHOD = 'native'

ERROR_MSG = '''\
Failed to bootstrap accent-auth. Error is logged at {log_file}.
'''


def save_exception_and_exit():
    with tempfile.NamedTemporaryFile(
        mode='w', prefix='accent-auth-bootstrap-', delete=False
    ) as log_file:
        traceback.print_exc(file=log_file)
        print(ERROR_MSG.format(log_file=log_file.name), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Initialize accent-auth')
    subparser = parser.add_subparsers(help='The action to execute', dest='action')
    subparser.add_parser('setup', help='deprecated')
    subparser.add_parser('complete')
    initial_user_parser = subparser.add_parser('initial-user')
    initial_user_parser.add_argument(
        '--uri', default=os.getenv('ACCENT_AUTH_BOOTSTRAP_URI')
    )
    initial_user_parser.add_argument(
        '--username', default=os.getenv('ACCENT_AUTH_BOOTSTRAP_USERNAME', USERNAME)
    )
    initial_user_parser.add_argument(
        '--password',
        default=os.getenv('ACCENT_AUTH_BOOTSTRAP_PASSWORD', random_string(28)),
    )
    initial_user_parser.add_argument(
        '--purpose', default=os.getenv('ACCENT_AUTH_BOOTSTRAP_PURPOSE', PURPOSE)
    )
    initial_user_parser.add_argument(
        '--policy-slug',
        default=os.getenv('ACCENT_AUTH_BOOTSTRAP_POLICY_SLUG', DEFAULT_POLICY_SLUG),
    )

    args = parser.parse_args()

    if args.action == 'setup':
        print('`accent-auth-bootstrap setup` command is no longer needed')
    elif args.action == 'complete':
        try:
            complete()
        except Exception:
            save_exception_and_exit()
    elif args.action == 'initial-user':
        uri = args.uri or get_database_uri_from_config()
        try:
            create_initial_user(
                uri,
                args.username,
                args.password,
                args.purpose,
                AUTHENTICATION_METHOD,
                args.policy_slug,
            )
        except Exception:
            save_exception_and_exit()
    else:
        parser.print_help()


def get_database_uri_from_config():
    accent_auth_config = read_config_file_hierarchy(
        {'config_file': DEFAULT_ACCENT_AUTH_CONFIG_FILE}
    )
    return accent_auth_config['db_uri']


def create_initial_user(
    db_uri, username, password, purpose, authentication_method, policy_slug
):
    init_db(db_uri)
    dao = queries.DAO.from_defaults()
    policy_service = services.PolicyService(dao)
    user_service = services.UserService(dao)
    if user_service.verify_password(username, password):
        # Already bootstrapped, just skip
        return

    users = user_service.list_users(username=username)
    if users:
        raise Exception(f'User {username} already exists with different credential')

    user = user_service.new_user(
        enabled=True,
        username=username,
        password=password,
        purpose=purpose,
        authentication_method=authentication_method,
    )
    policy_uuid = policy_service.list(slug=policy_slug)[0].uuid
    user_service.add_policy(user['uuid'], policy_uuid)

    commit_or_rollback()


def complete():
    database_uri = get_database_uri_from_config()

    if os.path.exists(CLI_CONFIG_FILENAME):
        # NOTE: Allow custom username/password or reuse previous one
        accent_auth_cli_config = parse_config_file(CLI_CONFIG_FILENAME)
        create_initial_user(
            database_uri,
            accent_auth_cli_config['auth']['username'],
            accent_auth_cli_config['auth']['password'],
            PURPOSE,
            AUTHENTICATION_METHOD,
            DEFAULT_POLICY_SLUG,
        )
    else:
        password = random_string(28)
        create_initial_user(
            database_uri,
            USERNAME,
            password,
            PURPOSE,
            AUTHENTICATION_METHOD,
            DEFAULT_POLICY_SLUG,
        )

        try:
            os.makedirs(CLI_CONFIG_DIR)
        except FileExistsError:
            pass

        cli_config = CLI_CONFIG.format(USERNAME, password)
        write_private_file(CLI_CONFIG_FILENAME, USER, cli_config)


def write_private_file(filename, username, content):
    try:
        user = getpwnam(username)
        uid = user.pw_uid
        gid = user.pw_gid
    except KeyError:
        raise Exception(f'Unknown user {username}')

    try:
        os.unlink(filename)
    except OSError:
        pass

    os.mknod(filename)
    os.chown(filename, uid, gid)
    with open(filename, 'w') as f:
        f.write(content)


def random_string(length):
    return ''.join(random.SystemRandom().choice(VALID_CHARS) for _ in range(length))
