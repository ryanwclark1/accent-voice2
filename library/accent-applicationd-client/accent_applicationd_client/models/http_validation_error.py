# Copyright 2025 Accent Communications
"""HTTP validation error model for the Accent applicationd client.
"""


from pydantic import BaseModel

from accent_applicationd_client.models.validation_error import ValidationError


class HTTPValidationError(BaseModel):
    """HTTP validation error model.

    Attributes:
        detail: List of validation errors

    """

    detail: list[ValidationError] | None = None

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
