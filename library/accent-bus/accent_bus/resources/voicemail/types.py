# resources/voicemail/types.py
from pydantic import BaseModel


class VoicemailFolderDict(BaseModel):
    """Represents a voicemail folder."""

    id: int
    name: str
    type: str


class VoicemailMessageDict(BaseModel):
    """Represents a voicemail message."""

    id: str
    caller_id_name: str
    caller_id_num: str
    duration: int
    timestamp: int  # Changed from tiemstamp
    folder: VoicemailFolderDict
