# resources/common/types.py
from typing import Annotated, Literal

from pydantic import BaseModel, Field

_string_formats = Literal["date", "date-time", "uuid"]


class Format(BaseModel):
    """Pydantic model for string formats.

    Attributes:
        format: The format of the string.

    """

    format: _string_formats | None = Field(default=None)


# Type aliases
UUIDStr = Annotated[str, Format(format="uuid")]
DateTimeStr = Annotated[str, Format(format="date-time")]
DateStr = Annotated[str, Format(format="date")]
