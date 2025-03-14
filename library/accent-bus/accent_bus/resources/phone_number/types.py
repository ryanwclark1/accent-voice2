# resources/phone_number/types.py

from pydantic import UUID4, BaseModel


class PhoneNumberDict(BaseModel):
    """Represents a phone number."""

    uuid: UUID4
    tenant_uuid: UUID4
    number: str
    caller_id_name: str | None = None
    main: bool
    shareable: bool
