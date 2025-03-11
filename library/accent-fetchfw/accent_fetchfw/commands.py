# commands.py
# Copyright 2025 Accent Communications

"""Command handling infrastructure for accent-fetchfw CLI."""

import argparse
import sys


def execute_command(command, args: list[str] | None = None) -> None:
    """Execute a command with the given arguments.

    Args:
        command: The command to execute
        args: Command line arguments (defaults to sys.argv[1:])

    """
    if args is None:
        args = sys.argv[1:]
    command_executor = CommandExecutor(command)
    command_executor.execute(args)


class CommandExecutor:
    """Executor for CLI commands."""

    def __init__(self, command) -> None:
        """Initialize the command executor.

        Args:
            command: The command to execute

        """
        self._command = command

    def execute(self, args: list[str]) -> None:
        """Execute the command with the given arguments.

        Args:
            args: Command line arguments

        """
        parser = self._command.create_parser()
        self._command.configure_parser(parser)

        subcommands = self._command.create_subcommands()
        self._command.configure_subcommands(subcommands)
        subcommands.configure_parser(parser)

        parsed_args = parser.parse_args(args)
        self._command.pre_execute(parsed_args)
        subcommands.execute(parsed_args)


class AbstractCommand:
    """Base class for all commands."""

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser for this command.

        Returns:
            An argument parser

        """
        return argparse.ArgumentParser()

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        """Configure the argument parser.

        Args:
            parser: The parser to configure

        """

    def create_subcommands(self) -> "Subcommands":
        """Create subcommands for this command.

        Returns:
            A Subcommands instance

        """
        return Subcommands()

    def configure_subcommands(self, subcommands: "Subcommands") -> None:
        """Configure subcommands for this command.

        Args:
            subcommands: The subcommands to configure

        Raises:
            Exception: This method must be overridden in derived classes

        """
        raise Exception("must be overriden in derived class")

    def pre_execute(self, parsed_args: argparse.Namespace) -> None:
        """Perform pre-execution setup.

        Args:
            parsed_args: The parsed arguments

        """


class Subcommands:
    """Collection of subcommands for a command."""

    def __init__(self) -> None:
        """Initialize the subcommands collection."""
        self._subcommands = []

    def add_subcommand(self, subcommand: "AbstractSubcommand") -> None:
        """Add a subcommand to the collection.

        Args:
            subcommand: The subcommand to add

        """
        self._subcommands.append(subcommand)

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        """Configure the parser with subcommand options.

        Args:
            parser: The parser to configure

        """
        subparsers = parser.add_subparsers(required=True, dest="_subcommand")
        for subcommand in self._subcommands:
            subcommand_parser = subparsers.add_parser(subcommand.name)
            subcommand_parser.set_defaults(_subcommand=subcommand)
            subcommand.configure_parser(subcommand_parser)

    def execute(self, parsed_args: argparse.Namespace) -> None:
        """Execute the selected subcommand.

        Args:
            parsed_args: The parsed arguments

        """
        subcommand = parsed_args._subcommand
        subcommand.execute(parsed_args)


class AbstractSubcommand:
    """Base class for all subcommands."""

    def __init__(self, name: str) -> None:
        """Initialize the subcommand.

        Args:
            name: The name of the subcommand

        """
        self.name = name

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        """Configure the parser for this subcommand.

        Args:
            parser: The parser to configure

        """

    def execute(self, parsed_args: argparse.Namespace) -> None:
        """Execute the subcommand.

        Args:
            parsed_args: The parsed arguments

        Raises:
            Exception: This method must be overridden in derived classes

        """
        raise Exception("must be overriden in derived class")
