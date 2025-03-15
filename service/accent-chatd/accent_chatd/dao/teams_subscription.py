# src/accent_chatd/dao/teams_subscription.py

from sqlalchemy import select

from accent_chatd.models.teams_subscription import TeamsSubscription

from .base import BaseDAO


class TeamsSubscriptionDAO(BaseDAO):
    async def create(self, subscription: TeamsSubscription) -> TeamsSubscription:
        async with self.session() as session:
            async with session.begin():
                session.add(subscription)
                await session.flush()
                await session.refresh(subscription)
                return subscription

    async def get_by_user_uuid(self, user_uuid: str) -> TeamsSubscription | None:
        async with self.session() as session:
            result = await session.execute(
                select(TeamsSubscription).where(
                    TeamsSubscription.user_uuid == user_uuid
                )
            )
            return result.scalars().first()

    async def get_by_subscription_id(
        self, subscription_id: str
    ) -> TeamsSubscription | None:
        async with self.session() as session:
            result = await session.execute(
                select(TeamsSubscription).where(
                    TeamsSubscription.subscription_id == subscription_id
                )
            )
            return result.scalars().first()

    async def update(self, subscription: TeamsSubscription) -> TeamsSubscription:
        async with self.session() as session:
            async with session.begin():
                session.add(subscription)
                return subscription

    async def delete(self, subscription: TeamsSubscription) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.delete(subscription)
