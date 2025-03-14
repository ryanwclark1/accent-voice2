# Copyright 2023 Accent Communications


"""A command-line interpreter that interact with provd servers."""


import builtins
import code
import os
import re
import readline
import sys
import types
from argparse import ArgumentParser
from pprint import pprint

from accent.config_helper import parse_config_file
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient

import accent_provd_cli.helpers as helpers
from accent_provd_cli import client as cli_client

DEFAULT_HISTFILE = os.path.expanduser('~/.accent_provd_cli')
DEFAULT_HISTFILESIZE = 500

_CONFIG = {
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/accent-auth-keys/accent-provd-cli-key.yml',
    },
    'provd': {
        'host': 'localhost',
        'port': 8666,
        'prefix': None,
        'https': False,
    },
}

# parse command line arguments
parser = ArgumentParser(usage='usage: %%prog [options] [hostname]')
parser.add_argument('--port', help='port number of the REST API')
parser.add_argument('--prefix', help='prefix to use to connect to provd')
parser.add_argument('--https', help='enable or disable HTTPS connection to provd')
parser.add_argument(
    '--verify',
    help='enable or disable verification of the certificate used by provd,'
    ' or path of the certificate to use for validation',
)
parser.add_argument('-c', '--command', help='specify the command to execute')
parser.add_argument(
    '--tests', action='store_true', default=False, help='import the tests module'
)

opts, args = parser.parse_known_args()


def _bool(value):
    if value in ['True', 'true', '1']:
        return True
    if value in ['False', 'false', '0']:
        return False
    return value


if args:
    _CONFIG['provd']['host'] = args[0]
if opts.port is not None:
    _CONFIG['provd']['port'] = int(opts.port)
if opts.prefix is not None:
    _CONFIG['provd']['prefix'] = int(opts.prefix)
if opts.https is not None:
    _CONFIG['provd']['https'] = _bool(opts.https)
if opts.verify is not None:
    _CONFIG['provd']['verify_certificate'] = _bool(opts.verify)

# # create client object
client = cli_client.new_cli_provisioning_client(_CONFIG['provd'])

# read key from key file and setup token renewer
key_file = parse_config_file(_CONFIG['auth'].pop('key_file'))
auth_client = AuthClient(
    username=key_file['service_id'], password=key_file['service_key'], **_CONFIG['auth']
)
token_renewer = TokenRenewer(auth_client, expiration=600)
token_renewer.subscribe_to_token_change(client.prov_client.set_token)


configs = client.configs()
devices = client.devices()
plugins = client.plugins()
parameters = client.parameters()


# create help
RAW_HELP_MAP = {
    None: """\
\x1b[1mDescription\x1b[0m
    You can interact with the provd server through 3 top-level objects:
        configs
        devices
        plugins

    Type help(object) (for example help(plugins)) for help about this object.

    Type dirr(object) to see all the 'public' attributes of this object.

\x1b[1mExamples\x1b[0m
    Get the list of installable plugins:

        plugins.installable()

    Synchronize the device 'dev1'

        devices['dev1'].synchronize()

    Get the raw config of config 'guest'

        configs['guest'].get_raw()

\x1b[1mNotes\x1b[0m
    This CLI is a plain python interpreter.
""",
    cli_client.Configs: """\
\x1b[1mDescription\x1b[0m
    Manage the configs.

\x1b[1mExamples\x1b[0m
    Get config 'foo'

        configs.get('foo')

    Get config 'foo' in raw form

        configs.get_raw('foo')

    Get config 'foo' as a config object

        configs['foo']

    List all known config

        configs.find()

    Add config 'foo'

        configs.add({'id': 'foo', 'parent_ids': [],
                     'raw_config.sip.lines.1.proxy_ip': '192.168.32.101'})

    Clone config 'foo' to 'bar'

        configs.clone('foo', 'bar')

    Update config 'foo' (warning: this is a replace operation)

        configs.update({'id': 'foo', 'parent_ids': [], 'raw_config': {})

    Remove config 'foo'

        configs.remove('foo')
""",
    cli_client.Config: """\
\x1b[1mDescription\x1b[0m
    Manage a particular config.

    This object is mostly useful if you want to do quick modifications to
    a specific config.

\x1b[1mExamples\x1b[0m
    Set the vlan ID parameter of config 'foo' to 100

        configs['foo'].set_config({'vlan.id': '100'})

    Unset the vlan ID parameter of config 'foo'

        configs['foo'].unset_config('vlan.id')

    Set the parent IDs of config 'foo' to 'base'

        configs['foo'].set_parents('base')

    Get the config 'foo'

        configs['foo'].get()

    Get the config 'foo' in raw form

        configs['foo'].get_raw()
""",
    cli_client.Devices: """\
\x1b[1mDescription\x1b[0m
    Manage the devices.

\x1b[1mExamples\x1b[0m
    Synchronize device 'foo'

        devices.synchronize('foo')

    Reconfigure device 'foo'

        devices.reconfigure('foo')

    Get device 'foo'

        devices.get('foo')

    Get device 'foo' as a device object

        devices['foo']

    List all known devices which are using 'accent-aastra-2.6.0.2010' plugin

        devices.find({'plugin': 'accent-aastra-2.6.0.2010'})

    Add device 'foo'

        devices.add({'id': 'foo', 'mac': '00:11:22:33:44:55'})

    Remove device 'foo'

        devices.remove('foo')

    Update device 'foo' (warning: this is a replace operation, roughly
    equivalent to a remove than an add)

        devices.update({'id': 'foo', 'mac': '00:11:22:33:44:55'})
""",
    cli_client.Device: """\
\x1b[1mDescription\x1b[0m
    Manage a particular device.

    This object is mostly useful if you want to do quick modifications to
    a specific device. It's always possible to do the same thing via the
    global devices object.

\x1b[1mExamples\x1b[0m
    Set the 'plugin' parameter of device 'foo' to 'accent-aastra-3.2.0.70'

        devices['foo'].set({'plugin': 'accent-aastra-3.2.0.70'})

    Unset the 'plugin' parameter of device 'foo'

        devices['foo'].unset('plugin')

    Synchronize device 'foo'

        devices['foo'].synchronize()

    Set and synchronize device 'foo'

        devices['foo'].set({'config': 'guest'}).synchronize()

    Get device 'foo'

        devices['foo'].get()
""",
    cli_client.Plugins: """\
\x1b[1mDescription\x1b[0m
    Manage the plugin subsystem.

\x1b[1mExamples\x1b[0m
    Install plugin 'accent-aastra-2.6.0.2010'

        plugins.install('accent-aastra-2.6.0.2010')

    Upgrade plugin 'accent-aastra-2.6.0.2010'

        plugins.upgrade('accent-aastra-2.6.0.2010')

    Uninstall plugin 'accent-aastra-2.6.0.2010'

        plugins.uninstall('accent-aastra-2.6.0.2010')

    Update the installable plugin list

        plugins.update()

    List the installable plugins

        plugins.installable()

    List the installed plugins

        plugins.installed()

    Get the plugin object for plugin 'accent-aastra-2.6.0.2010'

        plugins['accent-aastra-2.6.0.2010']
""",
    cli_client.Plugin: """\
\x1b[1mDescription\x1b[0m
    Manage a particular plugin.

\x1b[1mExamples\x1b[0m
    Install plugin-package '6731i-fw'

        plugins['accent-aastra-2.6.0.2010'].install('6731i-fw')

    Install all available plugin-packages

        plugins['accent-aastra-2.6.0.2010'].install_all()
""",
    cli_client.Parameters: """\
\x1b[1mDescription\x1b[0m
    Manage parameters of the provisioning server.

\x1b[1mExamples\x1b[0m
    Get the parameters description

        parameters.infos()

    Get the value of 'locale' parameter

        parameters.get('locale')

    Set the value of 'locale' parameter

        parameters.set('locale', 'en')

    Unset the 'locale' parameter

        parameters.unset('locale')
""",
}


class CLIHelp:
    def __init__(self, raw_help_map):
        self._help_map = self._build_help_map(raw_help_map)

    @staticmethod
    def _build_help_map(raw_help_map):
        res = {}
        for raw_k, raw_v in raw_help_map.items():
            v = raw_v.rstrip()
            if isinstance(raw_k, types.MethodType):
                res[raw_k.__func__] = v
            else:
                res[raw_k] = v
        return res

    def __call__(self, obj=None):
        help_map = self._help_map
        if obj in help_map:
            print(help_map[obj])
        elif type(obj) in help_map:
            print(help_map[type(obj)])
        elif isinstance(obj, types.MethodType) and obj.__func__ in help_map:
            print(help_map[obj.__func__])
        else:
            print(f'No help for object "{obj}"')

    def __repr__(self):
        return 'Type help() for help, or help(object) for help about object.'


cli_help = CLIHelp(RAW_HELP_MAP)


# define a dirr command
def dirr(obj):
    return list(name for name in dir(obj) if not name.startswith('_'))


# initialize the helpers module
helpers._init_module(configs, devices, plugins)


# import and initialize the tests module
if opts.tests:
    import accent_provd_cli.plugin as plugin_tests

    plugin_tests._init_module(configs, devices, plugins)


# change interpreter prompt
sys.ps1 = 'accent-provd-cli> '
sys.ps2 = '....... '


# change display hook
def my_displayhook(value):
    if value is not None:
        builtins._ = value
        pprint(value)


sys.displayhook = my_displayhook


# define the CLI global names (without actually inserting them)
cli_globals = {
    'configs': configs,
    'devices': devices,
    'plugins': plugins,
    'parameters': parameters,
    'help': cli_help,
    'python_help': builtins.help,
    '__builtins__': builtins,
    'dirr': dirr,
    'helpers': helpers,
    'options': cli_client.OPTIONS,
    'pprint': pprint,
}

if opts.tests:
    cli_globals['tests'] = plugin_tests


# define completer for readline auto-completion
class Completer:
    # This is largely taken from the rlcompleter module
    def __init__(self, namespace):
        if not isinstance(namespace, dict):
            raise TypeError('namespace must be a dictionary')

        self.namespace = namespace

    def complete(self, text, state):
        if state == 0:
            if "." in text:
                self.matches = self.attr_matches(text)
            else:
                self.matches = self.global_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def _callable_postfix(self, val, word):
        if hasattr(val, '__call__'):
            word = word + "("
        return word

    def global_matches(self, text):
        matches = []
        for word, val in list(self.namespace.items()):
            if word.startswith(text) and word != "__builtins__":
                matches.append(self._callable_postfix(val, word))
        return matches

    def attr_matches(self, text):
        m = re.match(r"(\w+(\.\w+)*)\.(\w*)", text)
        if not m:
            return []
        expr, attr = m.group(1, 3)
        try:
            thisobject = eval(expr, self.namespace)
        except Exception:
            return []

        # get the content of the object, except __builtins__
        words = dirr(thisobject)
        if "__builtins__" in words:
            words.remove("__builtins__")

        if hasattr(thisobject, '__class__'):
            words.extend(get_class_members(thisobject.__class__))
        matches = []
        for word in words:
            if word.startswith(attr) and hasattr(thisobject, word):
                val = getattr(thisobject, word)
                word = self._callable_postfix(val, f"{expr}.{word}")
                matches.append(word)
        return matches


def get_class_members(klass):
    ret = dirr(klass)
    if hasattr(klass, '__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret


completer = Completer(cli_globals)
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')


# read history file
# purge history from previous raw_input calls, etc
readline.clear_history()
try:
    readline.read_history_file(DEFAULT_HISTFILE)
except OSError:
    # can't read or no such file
    try:
        # create new file rw only by user
        os.close(os.open(DEFAULT_HISTFILE, os.O_WRONLY, 0o600))
    except OSError:
        pass


# create interpreter and interact with user
class CustomInteractiveConsole(code.InteractiveConsole):
    def write(self, data):
        sys.stdout.write(data)


with token_renewer:
    # # test connectivity
    try:
        plugins.installable()
    except Exception as e:
        print('Error while connecting to accent-provd:', e, file=sys.stderr)
        sys.exit(1)
    if opts.command:
        exec(opts.command, cli_globals)
    else:
        cli = CustomInteractiveConsole(cli_globals)
        cli.interact('')


# save history file
readline.set_history_length(DEFAULT_HISTFILESIZE)
try:
    readline.write_history_file(DEFAULT_HISTFILE)
except OSError:
    print('warning: could not save history')
