#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Command-line interface for the Accent Configuration Generator client."""

import argparse
import asyncio
import configparser
import logging
import sys
from typing import Any

from accent_confgend_client.client import AsyncConfgendClient, ConfgendClient
from accent_confgend_client.exceptions import ConfgendError
from accent_confgend_client.models import ConfgendConfig

DEFAULT_CONFIG_FILE = "/etc/accent-confgend-client/config.conf"

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Set up logging for the CLI application.

    Args:
        verbose: Whether to enable verbose logging.

    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments.

    """
    parser = argparse.ArgumentParser(
        description="Accent Configuration Generator Client"
    )
    parser.add_argument(
        "-c",
        "--config-file",
        default=DEFAULT_CONFIG_FILE,
        help=f"Path to the config file (default: {DEFAULT_CONFIG_FILE})",
    )
    parser.add_argument("-p", "--port", type=int, help="Server port")
    parser.add_argument("--host", help="Server hostname or IP address")
    parser.add_argument(
        "-t", "--timeout", type=float, help="Connection timeout in seconds"
    )
    parser.add_argument(
        "--use-https", action="store_true", help="Use HTTPS for connection"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "-a", "--async", action="store_true", dest="use_async", help="Use async client"
    )
    parser.add_argument(
        "filename", metavar="frontend/conffile", help="Path to the configuration file"
    )
    parser.add_argument(
        "--cached",
        action="store_true",
        help="Use the cached version of the file if it exists. "
        "If there is no cached version, a new one will be generated",
    )
    parser.add_argument(
        "--invalidate",
        action="store_true",
        help="Invalidates the cached version of this configuration file",
    )
    parser.add_argument(
        "-o", "--output", help="Write output to the specified file instead of stdout"
    )

    return parser.parse_args()


def read_config_file(filename: str) -> dict[str, Any]:
    """Read configuration from a file.

    Args:
        filename: Path to the configuration file.

    Returns:
        Dictionary with configuration values.

    """
    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(filename)

    config = {}
    if cfg_parser.has_section("confgen"):
        if cfg_parser.has_option("confgen", "server"):
            config["host"] = cfg_parser.get("confgen", "server")
        if cfg_parser.has_option("confgen", "port"):
            config["port"] = cfg_parser.getint("confgen", "port")
        if cfg_parser.has_option("confgen", "timeout"):
            config["timeout"] = cfg_parser.getfloat("confgen", "timeout")
        if cfg_parser.has_option("confgen", "use_https"):
            config["use_https"] = cfg_parser.getboolean("confgen", "use_https")

    return config


async def async_main() -> int:
    """Main entry point for the async CLI application.

    Returns:
        Exit code.

    """
    args = parse_args()
    setup_logging(args.verbose)

    try:
        file_config = read_config_file(args.config_file)

        # Command line args override file config
        config_dict = {}
        for key in ["host", "port", "timeout", "use_https"]:
            if hasattr(args, key) and getattr(args, key) is not None:
                config_dict[key] = getattr(args, key)

        # Merge configs with command line taking precedence
        config = {**file_config, **config_dict}
        confgend_config = ConfgendConfig(**config)

        logger.debug(f"Using configuration: {confgend_config}")

        async with AsyncConfgendClient(confgend_config) as client:
            response = await client.get_config(
                args.filename, invalidate=args.invalidate, cached=args.cached
            )

            if args.output:
                with open(args.output, "wb") as f:
                    f.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)

        return 0

    except ConfgendError as e:
        logger.error(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


def main() -> int:
    """Main entry point for the CLI application.

    Returns:
        Exit code.

    """
    args = parse_args()
    setup_logging(args.verbose)

    if getattr(args, "use_async", False):
        return asyncio.run(async_main())

    try:
        file_config = read_config_file(args.config_file)

        # Command line args override file config
        config_dict = {}
        for key in ["host", "port", "timeout", "use_https"]:
            if hasattr(args, key) and getattr(args, key) is not None:
                config_dict[key] = getattr(args, key)

        # Merge configs with command line taking precedence
        config = {**file_config, **config_dict}
        confgend_config = ConfgendConfig(**config)

        logger.debug(f"Using configuration: {confgend_config}")

        with ConfgendClient(confgend_config) as client:
            response = client.get_config(
                args.filename, invalidate=args.invalidate, cached=args.cached
            )

            if args.output:
                with open(args.output, "wb") as f:
                    f.write(response.content)
            else:
                sys.stdout.buffer.write(response.content)

        return 0

    except ConfgendError as e:
        logger.error(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
