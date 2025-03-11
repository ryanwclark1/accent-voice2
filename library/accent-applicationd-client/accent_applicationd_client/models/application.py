# Copyright 2025 Accent Communications
"""Application model for the Accent applicationd client.
"""

from pydantic import BaseModel


class Application(BaseModel):
    """Application model.

    Attributes:
        uuid: The UUID of the application

    """

    uuid: str

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
