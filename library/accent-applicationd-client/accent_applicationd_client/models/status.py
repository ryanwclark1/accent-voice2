# Copyright 2025 Accent Communications
"""Status model for the Accent applicationd client.
"""

from enum import Enum

from pydantic import BaseModel


class StatusEnum(str, Enum):
    """Status enumeration.

    Attributes:
        OK: The service is working correctly
        KO: The service has an issue

    """

    OK = "ok"
    KO = "ko"


class Status(BaseModel):
    """Status model.

    Attributes:
        state: The state of the service

    """

    state: StatusEnum

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
