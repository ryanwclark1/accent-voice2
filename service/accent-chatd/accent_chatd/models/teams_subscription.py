# src/accent_chatd/models/teams_subscription.py
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, relationship
from sqlalchemy.orm import Mapped, mapped_column

from accent_chatd.core.database import Base
from .user import User


class TeamsSubscription(Base):
    # __tablename__ defined in Base
    # id: Mapped[int] = mapped_column(Integer, primary_key=True) # id in base.
    user_uuid: Mapped[str] = mapped_column(
        String, ForeignKey("chatd_user.uuid", ondelete="CASCADE"), nullable=False)
    subscription_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    client_state: Mapped[str] = mapped_column(String, nullable=False)
    resource: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ms_teams_user_id: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="teams_subscriptions")

    def __repr__(self):
        return (
            f"<TeamsSubscription(user_uuid={self.user_uuid}, "
            f"subscription_id={self.subscription_id}, "
            f"expiration_date_time={self.expiration_date_time})>"
        )
