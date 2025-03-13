# file: accent_dao/resources/features/persistor.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import and_, not_, or_, select

from accent_dao.alchemy.features import Features
from accent_dao.resources.func_key.search import (
    FUNC_KEY_APPLICATIONMAP_FOREIGN_KEY,
    FUNC_KEY_FEATUREMAP_FOREIGN_KEY,
)
from accent_dao.resources.utils.search import CriteriaBuilderMixin

logger = logging.getLogger(__name__)


class FeaturesPersistor(CriteriaBuilderMixin):
    """Persistor class for Features model."""

    def __init__(self, session: Any) -> None:  # Use Any for session
        """Initialize FeaturesPersistor.

        Args:
            session: Database session (can be sync or async).

        """
        self.session = session

    async def find_all(self, section: str) -> list[Features]:
        """Find all features for a given section.

        Args:
            section: The section name.

        Returns:
            A list of Feature objects.

        """
        query = select(Features).filter(Features.category == section)
        query = query.filter(Features.var_val.is_not(None))
        query = query.order_by(Features.var_metric.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def edit_all(self, section: str, features: list[Features]) -> None:
        """Edit all features for a given section.

        Args:
            section: The section name.
            features: A list of Feature objects with updated values.

        """
        await self._delete_all_section(section)
        features = self._fill_default_values(section, features)
        features = await self._update_existing_foreign_key_features(features)

        for feature in features:
            self.session.add(feature)  # Use add for each feature

        await self.session.flush()

    def _fill_default_values(
        self, section: str, features: list[Features]
    ) -> list[Features]:
        """Fill default values for features.

        Args:
            section: The section name.
            features: List of Feature objects.

        Returns:
            List of Feature objects with default values filled.

        """
        for feature in features:
            feature.filename = "features.conf"
            feature.category = section
        return features

    async def _delete_all_section(self, section: str) -> None:
        """Delete all features in a given section, except those with foreign keys.

        Args:
            section: The section name.

        """
        query = select(Features).filter(Features.category == section)

        if section == "featuremap":
            query = query.filter(
                not_(Features.var_name.in_(FUNC_KEY_FEATUREMAP_FOREIGN_KEY))
            )
        elif section == "applicationmap":
            query = query.filter(
                not_(Features.var_name.in_(FUNC_KEY_APPLICATIONMAP_FOREIGN_KEY))
            )

        result = await self.session.execute(query)
        for feature in result.scalars().all():
            await self.session.delete(feature)

    async def _update_existing_foreign_key_features(
        self, features: list[Features]
    ) -> list[Features]:
        """Update existing features that have foreign key constraints.

        Args:
            features: List of Feature objects.

        Returns:
            List of updated Feature objects.

        """
        query = select(Features).filter(
            or_(
                and_(
                    Features.category == "featuremap",
                    Features.var_name.in_(FUNC_KEY_FEATUREMAP_FOREIGN_KEY),
                ),
                and_(
                    Features.category == "applicationmap",
                    Features.var_name.in_(FUNC_KEY_APPLICATIONMAP_FOREIGN_KEY),
                ),
            )
        )
        result = await self.session.execute(query)
        old_features = result.scalars().all()

        updated_features = []
        for feature in features:
            updated_features.append(feature)
            for old_feature in old_features:
                if (
                    old_feature.category == feature.category
                    and old_feature.var_name == feature.var_name
                ):
                    old_feature.var_val = feature.var_val
                    self._fix_commented(old_feature)
                    updated_features.remove(feature)
        return updated_features

    def _fix_commented(self, feature: Features) -> None:
        """Fix commented state for features.

        Args:
            feature: The Feature object.

        """
        feature.commented = 0
