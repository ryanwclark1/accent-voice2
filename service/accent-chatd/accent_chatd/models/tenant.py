# src/accent_chatd/models/tenant.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_chatd.core.database import Base


class Tenant(Base):
    # __tablename__ defined in Base class
    # id = Column(Integer, primary_key=True)  # Defined in Base
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Tenant(id={self.id!r}, uuid={self.uuid!r})"
