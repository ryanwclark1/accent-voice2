# resources/user_external_app/types.py
from pydantic import BaseModel


class ExternalAppDict(BaseModel):
    """Represents an external application."""

    name: str
