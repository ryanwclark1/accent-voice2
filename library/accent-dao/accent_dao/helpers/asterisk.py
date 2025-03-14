# helpers/asterisk.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from collections.abc import Iterable, Sized
from functools import cached_property
from typing import Any, ClassVar, Protocol, cast

from accent_dao.helpers import errors

# Type aliases
OptionPair = list[str]
Options = list[OptionPair]

# Constants
_TRUTH_VALUES = [
    "yes",
    "true",
    "y",
    "t",
    "1",
    "on",
]
_OPTION_PAIR_LENGTH = 2
_LIST_OF_PAIR_ERROR = "list of pair of strings"


def convert_ast_true_to_int(value: str) -> int:
    """Convert an Asterisk boolean string to an integer.

    Args:
        value: The string value to convert.

    Returns:
        int: 1 if the value is in the list of Asterisk truth values, 0 otherwise.

    """
    return int(value in _TRUTH_VALUES)


def convert_int_to_ast_true(value: int | bool) -> str:
    """Convert an integer or boolean to an Asterisk boolean string.

    Args:
        value: The integer or boolean value to convert.

    Returns:
        str: 'yes' if the value is truthy, 'no' otherwise.

    """
    if value:
        return "yes"
    return "no"


class HasTable(Protocol):
    """Protocol for SQLAlchemy models with a __table__ attribute."""

    @property
    def __table__(self) -> Any:
        """Get the SQLAlchemy table metadata.

        Returns:
            Table metadata object with columns attribute.

        """
        ...


class AsteriskOptionsMixin:
    """Mixin class for handling Asterisk options in SQLAlchemy models.

    This mixin provides methods for managing Asterisk configuration options,
    including native options stored in database columns and extra options
    stored as separate entities.

    Attributes:
        EXCLUDE_OPTIONS: Set of option names to exclude from processing.
        EXCLUDE_OPTIONS_CONFD: Set of option names to exclude from the ConFD API.
        AST_TRUE_INTEGER_COLUMNS: Set of columns that should be treated as boolean
            values with Asterisk's yes/no format.
        _options: List of extra options not mapped to model columns.

    """

    EXCLUDE_OPTIONS: ClassVar[set[str]] = set()
    EXCLUDE_OPTIONS_CONFD: ClassVar[set[str]] = set()
    AST_TRUE_INTEGER_COLUMNS: ClassVar[set[str]] = set()
    _options: list[OptionPair]

    def __init__(self) -> None:
        """Initialize the mixin with empty options list."""
        self._options = []

    @cached_property
    def options(self) -> Options:
        """Get all options for this object.

        Returns:
            A list of option pairs [name, value].

        """
        return self.all_options(self.EXCLUDE_OPTIONS_CONFD)

    def set_options(self, option_names: set[str], options: list[list[str]]) -> None:
        """Set multiple options.

        Args:
            option_names: Set of valid native option names.
            options: List of option pairs [name, value] to set.

        Raises:
            InputError: If options is not an iterable or any option is invalid.

        """
        self.validate_options(options)
        for option in options:
            self.validate_option(option)
            column, value = option
            if column in option_names:
                self.set_native_option(column, value)
            else:
                self.add_extra_option(column, value)

    def all_options(self, exclude: set[str] | None = None) -> Options:
        """Get all options, including both native and extra options.

        Args:
            exclude: Optional set of option names to exclude.

        Returns:
            A list of option pairs [name, value].

        """
        native_options = list(self.native_options(exclude))
        return native_options + self._options

    def native_options(self, exclude: set[str] | None = None) -> Iterable[OptionPair]:
        """Get native options mapped to database columns.

        Args:
            exclude: Optional set of option names to exclude.

        Yields:
            Option pairs [name, value] for native options with non-None values.

        """
        for column in self.native_option_names(exclude):
            value = self.native_option(column)
            if value is not None:
                yield [column, value]

    def native_option(self, column_name: str) -> str | None:
        """Get the value of a native option.

        Args:
            column_name: The name of the column/option.

        Returns:
            The string value of the option, or None if the value is None or empty.

        """
        value = getattr(self, self._attribute(column_name), None)
        if value is not None and value != "":
            if column_name in self.AST_TRUE_INTEGER_COLUMNS:
                return convert_int_to_ast_true(value)
            return str(value)
        return None

    def update_options(self, options: Options) -> None:
        """Set the options for this object.

        Args:
            options: A list of option pairs [name, value].

        """
        option_names = self.native_option_names(self.EXCLUDE_OPTIONS_CONFD)
        self.reset_options()
        self.set_options(option_names, options)

    def reset_options(self) -> None:
        """Reset all options to their default values."""
        self.reset_extra_options()
        self.reset_native_options()

    def reset_extra_options(self) -> None:
        """Reset extra options to an empty list."""
        self._options = []

    def reset_native_options(self) -> None:
        """Reset native options to their default values."""
        defaults = self.option_defaults()
        for column in self.native_option_names(self.EXCLUDE_OPTIONS_CONFD):
            value = defaults.get(column, None)
            setattr(self, self._attribute(column), value)

    def validate_options(self, options: list[Any]) -> None:
        """Validate that options is an iterable.

        Args:
            options: The options to validate.

        Raises:
            InputError: If options is not an iterable.

        """
        error_msg = _LIST_OF_PAIR_ERROR
        if not isinstance(options, Iterable):
            msg = "options"
            raise errors.wrong_type(msg, error_msg)

    def validate_option(self, option: list[Any]) -> None:
        """Validate that an option is a pair of strings.

        Args:
            option: The option to validate.

        Raises:
            InputError: If option is not a pair of strings.

        """
        error_msg = _LIST_OF_PAIR_ERROR
        if not isinstance(option, list | tuple):
            msg = "options"
            raise errors.wrong_type(msg, error_msg)

        sized_option = cast(Sized, option)
        if len(sized_option) != _OPTION_PAIR_LENGTH:
            msg = "options"
            raise errors.wrong_type(msg, error_msg)

        for i in option:
            if not isinstance(i, str):
                not_str_msg = f"value '{i}' is not a string"
                msg = "options"
                raise errors.wrong_type(msg, not_str_msg)

    def set_native_option(self, column: str, value: str) -> None:
        """Set a native option value.

        Args:
            column: The name of the column/option.
            value: The string value to set.

        """
        if column in self.AST_TRUE_INTEGER_COLUMNS:
            int_value = convert_ast_true_to_int(value)
            setattr(self, self._attribute(column), int_value)
        else:
            setattr(self, self._attribute(column), value)

    def add_extra_option(self, name: str, value: str) -> None:
        """Add an extra option that is not mapped to a database column.

        Args:
            name: The name of the option.
            value: The value of the option.

        """
        self._options.append([name, value])

    def native_option_names(self, exclude: set[str] | None = None) -> set[str]:
        """Get the names of native options.

        Args:
            exclude: Optional set of option names to exclude.

        Returns:
            Set of native option names.

        """
        exclude_set = set(exclude or []).union(self.EXCLUDE_OPTIONS)

        # Need to cast self to HasTable to satisfy mypy
        table_obj = cast(HasTable, self)
        return {column.name for column in table_obj.__table__.columns} - exclude_set

    def option_defaults(self) -> dict[str, Any]:
        """Get default values for options from column defaults.

        Returns:
            Dictionary mapping column names to their default values.

        """
        defaults: dict[str, Any] = {}

        # Need to cast self to HasTable to satisfy mypy
        table_obj = cast(HasTable, self)
        for column in table_obj.__table__.columns:
            if column.server_default:
                defaults[column.name] = column.server_default.arg
        return defaults

    def _attribute(self, column_name: str) -> str:
        """Convert a column name to an attribute name.

        Args:
            column_name: The name of the column.

        Returns:
            The corresponding attribute name.

        """
        return column_name.replace("-", "_")
