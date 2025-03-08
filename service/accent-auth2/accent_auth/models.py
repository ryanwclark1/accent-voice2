# accent_auth/models.py
from pydantic import BaseModel, ConfigDict


class CustomBaseModel(BaseModel):
    """
    Custom base model for Pydantic, providing common configurations.

    Attributes:
        model_config (ConfigDict): Configuration dictionary for Pydantic.
            from_attributes (bool): Enable ORM mode (Pydantic v2).
            populate_by_name (bool): Allow populating fields by name and alias.
            json_schema_extra (dict): Provides extra information for JSON schema, like examples.
    """

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, json_schema_extra={"example": {}}
    )
