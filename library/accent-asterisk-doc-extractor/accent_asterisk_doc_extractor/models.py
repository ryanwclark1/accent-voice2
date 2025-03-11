# Copyright 2025 Accent Communications
"""Data models for Asterisk PJSIP documentation."""


from pydantic import BaseModel, Field


class PJSIPChoice(BaseModel):
    """Represents a choice option for a PJSIP configuration parameter.

    Attributes:
        name: The name of the choice.
        description: The description of the choice.

    """

    name: str
    description: str = ""


class PJSIPOption(BaseModel):
    """Represents a PJSIP configuration option.

    Attributes:
        name: The name of the option.
        default: The default value of the option, if any.
        synopsis: A brief description of the option.
        description: A detailed description of the option.
        note: Additional notes about the option.
        choices: A dictionary of available choices for this option.

    """

    name: str
    default: str | None = None
    synopsis: str = ""
    description: str = ""
    note: str = ""
    choices: dict[str, str] = Field(default_factory=dict)


class PJSIPSection(BaseModel):
    """Represents a section in PJSIP documentation.

    Attributes:
        name: The name of the section.
        options: A dictionary of options in this section.

    """

    name: str
    options: dict[str, PJSIPOption] = Field(default_factory=dict)


class PJSIPDocumentation(BaseModel):
    """Represents the complete PJSIP documentation.

    Attributes:
        sections: A dictionary of sections in the documentation.

    """

    sections: dict[str, dict[str, PJSIPOption]] = Field(default_factory=dict)
