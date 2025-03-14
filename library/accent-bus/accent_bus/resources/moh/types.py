# resources/moh/types.py
from pydantic import UUID4, BaseModel


class MOHDict(BaseModel):
    """Represents Music on Hold (MOH) information."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
