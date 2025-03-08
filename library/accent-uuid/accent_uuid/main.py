#! /usr/bin/python3
# Copyright 2023 Accent Communications

import os.path
import subprocess
import uuid

ACCENT_UUID_FILENAME = '/etc/profile.d/accent_uuid.sh'
ACCENT_UUID_FILE = '''\
export ACCENT_UUID={uuid}
'''
SYSTEM_CONF_FILENAME = '/etc/systemd/system.conf'


def _already_configured():
    try:
        if b'ACCENT_UUID' not in subprocess.check_output(['systemctl', 'show-environment']):
            return False
    except (subprocess.CalledProcessError, OSError):
        return False

    if not os.path.isfile(ACCENT_UUID_FILENAME):
        return False

    with open(SYSTEM_CONF_FILENAME, 'r') as f:
        return 'ACCENT_UUID' in f.read()


def _get_uuid():
    return str(uuid.uuid4())


def _set_systemd_environment(uuid):
    try:
        subprocess.call(['systemctl', 'set-environment', 'ACCENT_UUID={}'.format(uuid)])
    except (subprocess.CalledProcessError, OSError):
        # systemd is not running yet, a reboot is required anyway
        pass


def _set_system_conf(uuid):
    env_line = 'DefaultEnvironment='

    try:
        with open(SYSTEM_CONF_FILENAME, 'r') as f:
            original = list(f)
    except IOError:
        original = [env_line]

    with open(SYSTEM_CONF_FILENAME, 'w') as f:
        for line in original:
            if env_line not in line:
                f.write(line)
            elif line.startswith('#') or line.strip().endswith('='):
                f.write('{}"ACCENT_UUID={}"\n'.format(env_line, uuid))
            else:
                new_line = '{} "ACCENT_UUID={}"\n'.format(line.strip(), uuid)
                f.write(new_line)


def _set_etc_profile(uuid):
    content = ACCENT_UUID_FILE.format(uuid=uuid)
    with open(ACCENT_UUID_FILENAME, 'w') as f:
        f.write(content)


def main():
    if not _already_configured():
        uuid = _get_uuid()
        _set_etc_profile(uuid)
        _set_system_conf(uuid)
        _set_systemd_environment(uuid)


if __name__ == '__main__':
    main()
