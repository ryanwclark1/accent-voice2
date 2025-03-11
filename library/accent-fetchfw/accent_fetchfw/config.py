# config.py
# Copyright 2025 Accent Communications

"""Configuration handling for accent-fetchfw."""

from configparser import RawConfigParser
from typing import Any

from accent_fetchfw.params import ConfigSpec


def _new_config_spec() -> ConfigSpec:
    """Create a new configuration specification.

    Returns:
        A configured ConfigSpec instance

    """
    cfg_spec = ConfigSpec()

    # [general] section definition
    cfg_spec.add_param("general.root_dir", default="/")
    cfg_spec.add_param("general.db_dir", default="/var/lib/accent-fetchfw")
    cfg_spec.add_param("general.cache_dir", default="/var/cache/accent-fetchfw")

    @cfg_spec.add_param_decorator("general.auth_sections", default=[])
    def _auth_sections_fun(raw_value: str) -> list[str]:
        return raw_value.split()

    # [global_vars] section definition
    cfg_spec.add_section("global_vars")

    # [proxy] section definition
    cfg_spec.add_section("proxy")

    # dynamic [auth-section] definition (referenced by general.auth_sections)
    cfg_spec.add_dyn_param("auth-section", "uri", default=ConfigSpec.MANDATORY)
    cfg_spec.add_dyn_param("auth-section", "username", default=ConfigSpec.MANDATORY)
    cfg_spec.add_dyn_param("auth-section", "password", default=ConfigSpec.MANDATORY)

    # unknown section hook for dynamic auth sections
    @cfg_spec.set_unknown_section_hook_decorator
    def _unknown_section_hook(
        config_dict: dict[str, Any], section_id: str, section_dict: dict[str, Any]
    ) -> str | None:
        if section_id in config_dict["general.auth_sections"]:
            return "auth-section"
        return None

    return cfg_spec


# Global config specification
_CONFIG_SPEC = _new_config_spec()


def read_config(filename: str) -> dict[str, Any]:
    """Read configuration from a file.

    Args:
        filename: Path to the configuration file

    Returns:
        Dictionary of configuration parameters

    Raises:
        IOError: If the file cannot be read
        ParsingError: If the file is not a valid configuration file

    """
    config_parser = RawConfigParser()
    # case-sensitive options (used for section 'global_vars')
    config_parser.optionxform = str
    with open(filename) as f:
        config_parser.read_file(f)
    return _CONFIG_SPEC.read_config(config_parser)
