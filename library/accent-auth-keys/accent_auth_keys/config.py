# Copyright 2025 Accent Communications

"""Configuration handling for the Accent Auth Keys application."""

# TODO: Update config with Pydantic Settings
import os
from typing import Any

from accent.chain_map import ChainMap
from accent.config_helper import (
    parse_config_dir,
    read_config_file_hierarchy_accumulating_list,
)
from accent_auth_cli.config import _DEFAULT_CONFIG

SERVICES_CONFIG_FILE = "config.yml"
SERVICES_EXTRA_CONFIG = "conf.d"


def _read_user_config(parsed_args: Any) -> dict[str, Any]:
    """Read user configuration from a directory.

    Args:
        parsed_args: Parsed command line arguments.

    Returns:
        The user configuration as a dictionary.

    """
    if not parsed_args.accent_auth_cli_config:
        return {}
    configs = parse_config_dir(parsed_args.accent_auth_cli_config)
    return ChainMap(*configs)


def build(parsed_args: Any) -> ChainMap:
    """Build the final configuration by merging user and system configs.

    Args:
        parsed_args: Parsed command line arguments.

    Returns:
        The final configuration as a ChainMap.

    """
    user_file_config = _read_user_config(parsed_args)
    system_file_config = read_config_file_hierarchy_accumulating_list(
        ChainMap(user_file_config, _DEFAULT_CONFIG)
    )
    final_config = ChainMap(user_file_config, system_file_config, _DEFAULT_CONFIG)
    return final_config


def load_services(parsed_args: Any) -> dict[str, Any]:
    """Load services configuration.

    Args:
        parsed_args: Parsed command line arguments.

    Returns:
        The services configuration as a dictionary.

    """
    services_dir = parsed_args.config
    services_config = {
        "config_file": os.path.join(services_dir, SERVICES_CONFIG_FILE),
        "extra_config_files": os.path.join(services_dir, SERVICES_EXTRA_CONFIG),
    }
    services = read_config_file_hierarchy_accumulating_list(services_config)
    services.pop("config_file", None)
    services.pop("extra_config_files", None)
    return services
