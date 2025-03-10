# Copyright 2025 Accent Communications

"""Data models for the provisioning client."""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# Operation state constants
class OperationState(str, Enum):
    """Operation states for provisioning operations."""

    WAITING = "waiting"
    PROGRESS = "progress"
    SUCCESS = "success"
    FAIL = "fail"


class BaseOperation(BaseModel):
    """Base model for operations.

    Attributes:
        label: Operation label
        state: Current operation state
        current: Current progress count
        end: End progress count
        sub_operations: List of sub-operations

    """

    label: str | None = None
    state: str = OperationState.WAITING
    current: int | None = None
    end: int | None = None
    sub_operations: list[BaseOperation] = Field(default_factory=list, alias="sub_oips")

    def __str__(self) -> str:
        """String representation of the operation."""
        status = f"{self.label}: {self.state}" if self.label else f"{self.state}"
        if self.current is not None and self.end is not None:
            status += f" ({self.current}/{self.end})"

        if self.sub_operations:
            for sub_op in self.sub_operations:
                status += f"\n  {sub_op}"

        return status

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True


class ConfigEntry(BaseModel):
    """Model for configuration entries.

    Attributes:
        id: Configuration ID
        config_data: Configuration data

    """

    id: str
    config_data: dict[str, Any]


class DeviceEntry(BaseModel):
    """Model for device entries.

    Attributes:
        id: Device ID
        device_data: Device data

    """

    id: str
    device_data: dict[str, Any]


class PluginInfo(BaseModel):
    """Model for plugin information.

    Attributes:
        id: Plugin ID
        plugin_data: Plugin data

    """

    id: str
    plugin_data: dict[str, Any]


class ParamEntry(BaseModel):
    """Model for parameter entries.

    Attributes:
        name: Parameter name
        value: Parameter value

    """

    name: str
    value: Any


# Define regex pattern for parsing operation strings
PARSE_OIP_REGEX = re.compile(r"^(?:(\w+)\|)?(\w+)(?:;(\d+)(?:/(\d+))?)?")


def parse_operation(operation_string: str) -> BaseOperation:
    """Parse an operation string into a BaseOperation object.

    Args:
        operation_string: The operation string to parse

    Returns:
        Parsed BaseOperation

    Raises:
        ValueError: If the operation string format is invalid

    """
    m = PARSE_OIP_REGEX.search(operation_string)
    if not m:
        raise ValueError(f"Invalid progress string: {operation_string}")

    label, state, raw_current, raw_end = m.groups()
    raw_sub_ops = operation_string[m.end() :]
    current = int(raw_current) if raw_current is not None else None
    end = int(raw_end) if raw_end is not None else None

    sub_operations = (
        [
            parse_operation(sub_op_string)
            for sub_op_string in _split_top_parentheses(raw_sub_ops)
        ]
        if raw_sub_ops
        else []
    )

    return BaseOperation(
        label=label,
        state=state,
        current=current,
        end=end,
        sub_operations=sub_operations,
    )


def _split_top_parentheses(str_: str) -> list[str]:
    """Split a string by top-level parentheses.

    Args:
        str_: String to split

    Returns:
        List of substring contents between parentheses

    Raises:
        ValueError: If the parenthesis structure is invalid

    """
    idx = 0
    length = len(str_)
    result = []

    while idx < length:
        if str_[idx] != "(":
            raise ValueError(f"invalid character: {str_[idx]}")

        start_idx = idx
        idx += 1
        count = 1

        while count:
            if idx >= length:
                raise ValueError(f"unbalanced number of parentheses: {str_}")

            c = str_[idx]
            if c == "(":
                count += 1
            elif c == ")":
                count -= 1

            idx += 1

        end_idx = idx
        result.append(str_[start_idx + 1 : end_idx - 1])

    return result
