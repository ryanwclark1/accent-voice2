# params.py
# Copyright 2025 Accent Communications

"""Module to transform configuration file to configuration data.

This is a bit of an experiment to create an easy, declarative way to declare
the valid format and options of an INI configuration file.

This module is not fetchfw specific, so it could be used by other projects if
it's found to be useful and not just a waste of time.

That said, look in fetchfw.config and fetchfw.conf to see examples on how
to use this module.
"""

import collections
from collections.abc import Callable
from configparser import RawConfigParser
from typing import Any, TypeVar

T = TypeVar("T")


class ConfigSpec:
    """Represent a configuration file's specification."""

    NO_DEFAULT = object()
    MANDATORY = object()

    def __init__(self) -> None:
        """Initialize a configuration specification."""
        # A dictionary where keys are param ids and values are tuple
        # (default value, fun). fun takes one argument, raw_value.
        self._params: dict[str, tuple[Any, Callable[[str], Any] | None]] = {}

        # A dictionary where keys are section ids and values are fun. fun
        # takes two arguments, name and raw_value
        self._sections: dict[str, Callable[[str, str], Any] | None] = {}

        # A dictionary where keys are template ids and values are dictionaries
        # which keys are options ids and value are tuple (default value, fun)
        self._dyn_params = collections.defaultdict(dict)

        self._unknown_section_hook: Callable[[dict[str, Any], str, dict[str, Any]], str | None] | None = None

        self.add_param_decorator = self._create_param_decorator()
        self.add_dyn_param_decorator = self._create_dyn_param_decorator()
        self.add_section_decorator = self._create_section_decorator()
        self.set_unknown_section_hook_decorator = self._create_unknown_section_dec()

    def _create_param_decorator(self) -> Callable:
        """Create a decorator for adding parameters.

        Returns:
            Decorator function

        """

        def param_decorator(param_id: str, default: Any = NO_DEFAULT) -> Callable:
            def aux(fun: Callable[[str], Any]) -> Callable[[str], Any]:
                self.add_param(param_id, default, fun)
                return fun

            return aux

        return param_decorator

    def _create_dyn_param_decorator(self) -> Callable:
        """Create a decorator for adding dynamic parameters.

        Returns:
            Decorator function

        """

        def dyn_param_decorator(
            template_id: str, option_id: str, default: Any = NO_DEFAULT
        ) -> Callable:
            def aux(fun: Callable[[str], Any]) -> Callable[[str], Any]:
                self.add_dyn_param(template_id, option_id, default, fun)
                return fun

            return aux

        return dyn_param_decorator

    def _create_section_decorator(self) -> Callable:
        """Create a decorator for adding sections.

        Returns:
            Decorator function

        """

        def section_decorator(section_id: str) -> Callable:
            def aux(fun: Callable[[str, str], Any]) -> Callable[[str, str], Any]:
                self.add_section(section_id, fun)
                return fun

            return aux

        return section_decorator

    def _create_unknown_section_dec(self) -> Callable:
        """Create a decorator for setting the unknown section hook.

        Returns:
            Decorator function

        """

        def unknown_section_hook_decorator(
            fun: Callable[[dict[str, Any], str, dict[str, Any]], str | None],
        ) -> Callable[[dict[str, Any], str, dict[str, Any]], str | None]:
            self.set_unknown_section_hook(fun)
            return fun

        return unknown_section_hook_decorator

    def add_param(
        self,
        param_id: str,
        default: Any = NO_DEFAULT,
        fun: Callable[[str], Any] | None = None,
    ) -> None:
        """Add a parameter to the specification.

        Args:
            param_id: Parameter ID (section.option)
            default: Default value or NO_DEFAULT or MANDATORY
            fun: Function to process the raw value

        Raises:
            ValueError: If the parameter is invalid or already exists

        """
        if "." not in param_id:
            raise ValueError(f"no dot character in param: {param_id}")
        if param_id in self._params:
            raise ValueError(f"param has already been specified: {param_id}")
        self._params[param_id] = (default, fun)

    def add_dyn_param(
        self,
        template_id: str,
        option_id: str,
        default: Any = NO_DEFAULT,
        fun: Callable[[str], Any] | None = None,
    ) -> None:
        """Add a dynamic parameter to the specification.

        Args:
            template_id: Template ID
            option_id: Option ID
            default: Default value or NO_DEFAULT or MANDATORY
            fun: Function to process the raw value

        Raises:
            ValueError: If the parameter already exists

        """
        template_dict = self._dyn_params[template_id]
        if option_id in template_dict:
            raise ValueError(
                f"dyn param already been specified: {template_id}.{option_id}"
            )
        template_dict[option_id] = (default, fun)

    def add_section(
        self, section_id: str, fun: Callable[[str, str], Any] | None = None
    ) -> None:
        """Add a section to the specification.

        Args:
            section_id: Section ID
            fun: Function to process raw values

        Raises:
            ValueError: If the section is invalid or already exists

        """
        if "." in section_id:
            raise ValueError(f"dot character in section: {section_id}")
        if section_id in self._sections:
            raise ValueError(f"section has already been specified: {section_id}")
        self._sections[section_id] = fun

    def set_unknown_section_hook(
        self, fun: Callable[[dict[str, Any], str, dict[str, Any]], str | None]
    ) -> None:
        """Set a hook to process unknown sections.

        Args:
            fun: Function to process unknown sections

        """
        self._unknown_section_hook = fun

    def _process_param(self, param_id: str, raw_value: str) -> Any:
        """Process a parameter value.

        Args:
            param_id: Parameter ID
            raw_value: Raw value

        Returns:
            Processed value

        """
        assert param_id in self._params
        fun = self._params[param_id][1]
        if fun is None:
            return raw_value
        return fun(raw_value)

    def _process_section(self, section_id: str, option_id: str, raw_value: str) -> Any:
        """Process a section option value.

        Args:
            section_id: Section ID
            option_id: Option ID
            raw_value: Raw value

        Returns:
            Processed value

        """
        assert section_id in self._sections
        fun = self._sections[section_id]
        if fun is None:
            return raw_value
        return fun(option_id, raw_value)

    def _add_default_and_check_mandatory(self, config_dict: dict[str, Any]) -> None:
        """Add default values and check for mandatory parameters.

        Args:
            config_dict: Configuration dictionary to update

        Raises:
            ValueError: If a mandatory parameter is missing

        """
        for param_id, param_value in self._params.items():
            if param_id not in config_dict:
                default = param_value[0]
                if default is self.MANDATORY:
                    raise ValueError(f"missing parameter: {param_id}")
                if default is self.NO_DEFAULT:
                    pass
                else:
                    config_dict[param_id] = default

    def read_config(self, config_parser: RawConfigParser) -> dict[str, Any]:
        """Read a configuration into a dictionary.

        Args:
            config_parser: Parsed configuration

        Returns:
            Dictionary of parameter values

        Raises:
            ValueError: If the configuration is invalid

        """
        config_dict = {}
        unknown_sections = collections.defaultdict(dict)
        for section_id in config_parser.sections():
            for option_id, raw_value in config_parser.items(section_id):
                param_id = f"{section_id}.{option_id}"
                if param_id in self._params:
                    config_dict[param_id] = self._process_param(param_id, raw_value)
                elif section_id in self._sections:
                    config_dict[param_id] = self._process_section(
                        section_id, option_id, raw_value
                    )
                else:
                    unknown_sections[section_id][option_id] = raw_value
        self._add_default_and_check_mandatory(config_dict)

        # Unknown section handling
        if unknown_sections:
            if self._unknown_section_hook:
                for section_id, section_dict in unknown_sections.items():
                    template_id = self._unknown_section_hook(
                        config_dict, section_id, section_dict
                    )
                    if template_id in self._dyn_params:
                        cur_dyn_params = self._dyn_params[template_id]
                        for option_id, raw_value in section_dict.items():
                            if option_id in cur_dyn_params:
                                fun = cur_dyn_params[option_id][1]
                                param_id = f"{section_id}.{option_id}"
                                if fun is None:
                                    config_dict[param_id] = raw_value
                                else:
                                    config_dict[param_id] = fun(raw_value)
                            else:
                                raise ValueError(
                                    f"unknown dynamic option {option_id} for template {template_id}"
                                )
                        for option_id, (default, _) in cur_dyn_params.items():
                            param_id = f"{section_id}.{option_id}"
                            if param_id not in config_dict:
                                if default is self.MANDATORY:
                                    raise ValueError(
                                        f"missing dyn parameter: {param_id}"
                                    )
                                if default is self.NO_DEFAULT:
                                    pass
                                else:
                                    config_dict[param_id] = default
                    else:
                        raise ValueError(
                            f"unknown template {template_id} returned for section {section_id}"
                        )
            else:
                raise ValueError(f"unknown sections: {list(unknown_sections.keys())}")
        return config_dict

    def read_config_from_filename(self, filename: str) -> dict[str, Any]:
        """Read a configuration from a file.

        Args:
            filename: Path to the configuration file

        Returns:
            Dictionary of parameter values

        Raises:
            IOError: If the file cannot be read
            ValueError: If the configuration is invalid

        """
        config_parser = RawConfigParser()
        with open(filename) as f:
            config_parser.read_file(f)
        return self.read_config(config_parser)


def filter_section(config_dict: dict[str, Any], section_id: str) -> dict[str, Any]:
    """Filter a configuration dictionary by section.

    Args:
        config_dict: Configuration dictionary
        section_id: Section ID to filter

    Returns:
        Dictionary of section options

    Raises:
        ValueError: If the section ID is invalid

    """
    if "." in section_id:
        raise ValueError(f"dot character in section: {section_id}")
    result = {}
    dot_section_id = section_id + "."
    dot_section_id_len = len(dot_section_id)
    for param_id, value in config_dict.items():
        if param_id.startswith(dot_section_id):
            result[param_id[dot_section_id_len:]] = value
    return result


_BOOL_TRUE = ["True", "true"]
_BOOL_FALSE = ["False", "false"]


def bool_(raw_value: str) -> bool:
    """Convert a string to a boolean.

    Args:
        raw_value: String to convert

    Returns:
        Boolean value

    Raises:
        ValueError: If the string is not a valid boolean

    """
    if raw_value in _BOOL_TRUE:
        return True
    if raw_value in _BOOL_FALSE:
        return False
    raise ValueError(f'invalid boolean raw value "{raw_value}"')
