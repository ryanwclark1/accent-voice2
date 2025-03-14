# resources/common/schemas.py
from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    """Represents a generic event.

    Attributes:
        name (str): The name of the event.
        data (dict): Event payload.

    """

    name: str
    data: dict[str, Any]
