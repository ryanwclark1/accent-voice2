#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Utility functions for the Accent Configuration Generator client."""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

import configparser
from accent_confgend_client.models import ConfgendConfig

logger = logging.getLogger(__name__)


def load_config_from_file(config_file: str) -> ConfgendConfig:
    """
    Load configuration from a file.

    Args:
        config_file: Path to the configuration file.

    Returns:
        ConfgendConfig object.
    """
    config_dict = {}

    if config_file and Path(config_file).exists():
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(config_file)

        if cfg_parser.has_section("confgen"):
            if cfg_parser.has_option("confgen", "server"):
                config_dict["host"] = cfg_parser.get("confgen", "server")
            if cfg_parser.has_option("confgen", "port"):
                config_dict["port"] = cfg_parser.getint("confgen", "port")
            if cfg_parser.has_option("confgen", "timeout"):
                config_dict["timeout"] = cfg_parser.getfloat("confgen", "timeout")
            if cfg_parser.has_option("confgen", "use_https"):
                config_dict["use_https"] = cfg_parser.getboolean("confgen", "use_https")

    return ConfgendConfig(**config_dict)
