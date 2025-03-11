# Copyright 2025 Accent Communications
"""Validation error models for the Accent applicationd client.
"""

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model.

    Attributes:
        loc: The location of the error
        msg: The error message
        type: The error type

    """

    loc: list[str]
    msg: str
    type: str

    # For backward compatibility
    def to_dict(self) -> dict:
        """Return model properties as a dict.

        Returns:
            Dictionary representation of the model

        """
        return self.model_dump()

    def to_str(self) -> str:
        """Return string representation of the model.

        Returns:
            String representation

        """
        return str(self.model_dump())
