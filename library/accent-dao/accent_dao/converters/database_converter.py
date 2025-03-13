# converters/database_converter.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import Any, Generic, Protocol, TypeVar, cast

T = TypeVar("T")
S = TypeVar("S")
K = TypeVar("K")  # Key type for mappings


class HasAttributes(Protocol):
    """Protocol for objects that support attribute access."""

    def __getattr__(self, name: str) -> Any:
        """Get attribute by name.

        Args:
            name: Attribute name to get

        Returns:
            The attribute value

        """
        ...

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute by name.

        Args:
            name: Attribute name to set
            value: Value to assign to the attribute

        """
        ...


class DatabaseConverter(Generic[T, S]):
    """Converter for mapping between database and model objects.

    This class handles bidirectional conversion between database schema objects
    and domain model objects based on a provided attribute mapping.
    """

    def __init__(
        self, mapping: dict[str, str], schema: type[S], model: type[T]
    ) -> None:
        """Initialize the database converter.

        Args:
            mapping: Dictionary mapping from schema attribute names to model
                attribute names
            schema: Class for the database schema objects
            model: Class for the domain model objects

        """
        self.schema = schema
        self.model = model

        # Create reverse mapping for model to schema conversion
        model_mapping = {value: key for key, value in mapping.items()}

        self.db_mapping = mapping
        self.model_mapping = model_mapping

    def to_model(self, db_row: S) -> T:
        """Convert a database row to a model object.

        Args:
            db_row: Database schema object to convert

        Returns:
            Converted model object

        Raises:
            ValueError: If a required attribute is missing

        """
        db_columns = self._extract_columns(
            cast(HasAttributes, db_row), set(self.db_mapping.keys())
        )
        model_columns = self._remap_columns(db_columns, self.db_mapping)
        return self.model(**model_columns)

    def to_source(self, model: T) -> S:
        """Convert a model object to a database schema object.

        Args:
            model: Model object to convert

        Returns:
            Converted database schema object

        Raises:
            ValueError: If a required attribute is missing

        """
        model_columns = self._extract_columns(
            cast(HasAttributes, model), set(self.model_mapping.keys())
        )
        db_columns = self._remap_columns(model_columns, self.model_mapping)
        return self.schema(**db_columns)

    def update_model(self, model: T, db_row: S) -> None:
        """Update a model object with values from a database row.

        Args:
            model: Model object to update
            db_row: Database schema object to get values from

        Raises:
            ValueError: If a required attribute is missing

        """
        db_columns = self._extract_columns(
            cast(HasAttributes, db_row), set(self.db_mapping.keys())
        )
        model_columns = self._remap_columns(db_columns, self.db_mapping)
        self._update_object(model_columns, cast(HasAttributes, model))

    def update_source(self, db_row: S, model: T) -> None:
        """Update a database schema object with values from a model.

        Args:
            db_row: Database schema object to update
            model: Model object to get values from

        Raises:
            ValueError: If a required attribute is missing

        """
        model_columns = self._extract_columns(
            cast(HasAttributes, model), set(self.model_mapping.keys())
        )
        db_columns = self._remap_columns(model_columns, self.model_mapping)
        self._update_object(db_columns, cast(HasAttributes, db_row))

    def _extract_columns(
        self, source_object: HasAttributes, columns: set[str]
    ) -> dict[str, Any]:
        """Extract column values from a source object.

        Args:
            source_object: Object to extract values from
            columns: Set of column names to extract

        Returns:
            Dictionary of column names to values

        Raises:
            ValueError: If a column doesn't exist in the source object

        """
        extracted_values: dict[str, Any] = {}
        for column_name in columns:
            if not hasattr(source_object, column_name):
                error_msg = (
                    f"Column {column_name} does not exist in object "
                    f"{type(source_object)}"
                )
                raise ValueError(error_msg)
            extracted_values[column_name] = getattr(source_object, column_name)
        return extracted_values

    def _remap_columns(
        self, columns: dict[str, Any], mapping: dict[str, str]
    ) -> dict[str, Any]:
        """Remap column names using a mapping dictionary.

        Args:
            columns: Dictionary of source column names to values
            mapping: Dictionary mapping from source column names to
                destination column names

        Returns:
            Dictionary with remapped column names

        """
        mapped_columns: dict[str, Any] = {}
        for column_name, value in columns.items():
            key = mapping[column_name]
            mapped_columns[key] = value
        return mapped_columns

    def _update_object(
        self, values: dict[str, Any], destination: HasAttributes
    ) -> None:
        """Update an object with values from a dictionary.

        Args:
            values: Dictionary of attribute names to values
            destination: Object to update with values

        """
        for key, value in values.items():
            setattr(destination, key, value)
