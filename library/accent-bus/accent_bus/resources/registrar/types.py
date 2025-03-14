# resources/registrar/types.py
from pydantic import BaseModel, Field


class RegistrarDict(BaseModel):
    """Represents registrar configuration."""

    id: str
    deletable: bool
    name: str
    main_host: str
    main_port: int
    backup_host: str
    backup_port: int
    proxy_main_host: str
    proxy_main_port: int
    proxy_backup_host: str
    proxy_backup_port: int
    outbound_proxy_host: str
    outbound_proxy_port: int
