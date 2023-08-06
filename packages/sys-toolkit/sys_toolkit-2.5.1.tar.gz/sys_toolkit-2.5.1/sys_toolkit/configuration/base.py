#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Loaders for ini, json and yaml format configuration files
"""
import os
import re

from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple

from sys_toolkit.logger import DEFAULT_TARGET_NAME

from ..base import LoggingBaseClass
from ..exceptions import ConfigurationError

# Pattern to validate configuration keys
RE_CONFIGURATIION_KEY = re.compile('^[a-zA-Z0-9_]+$')


class ConfigurationItemContainer(LoggingBaseClass):
    """
    Base class for containers of settings
    """
    __dict_loader_class__ = None
    """Loader class for dictionaries in configuration"""
    __list_loader_class__ = None
    """Loader class for lists in configuration"""
    __float_settings__: Tuple[str] = ()
    """Tuple of settings loaded as floats"""
    __integer_settings__: Tuple[str] = ()
    """Tuple of settings loaded as integers"""
    __path_settings__: Tuple[str] = ()
    """Tuple of settings loaded as pathlib.Path"""

    def __init__(self,
                 parent: Optional[LoggingBaseClass] = None,
                 debug_enabled: bool = False,
                 silent: bool = False,
                 logger: str = DEFAULT_TARGET_NAME) -> None:
        self.__attributes__ = []
        self.__parent__ = parent
        super().__init__(debug_enabled, silent, logger)

    @property
    def __config_root__(self) -> LoggingBaseClass:
        """
        Return configuration root item via parent links
        """
        parent = getattr(self, '__parent__', None)
        if parent is None:
            return self
        while getattr(parent, '__parent__', None) is not None:
            parent = getattr(parent, '__parent__', None)
        return parent

    @property
    def __dict_loader__(self) -> 'ConfigurationSection':
        """
        Return loader for dict items
        """
        if self.__dict_loader_class__ is not None:
            return self.__dict_loader_class__
        return ConfigurationSection

    @property
    def __list_loader__(self) -> 'ConfigurationList':
        """
        Return loader for list items
        """
        if self.__list_loader_class__ is not None:
            return self.__list_loader_class__
        return ConfigurationList

    @staticmethod
    def default_formatter(value) -> str:
        """
        Default formatter for variables

        By default trims whitespace from strings and sets empty strings to None
        """
        if isinstance(value, str):
            value = value.strip()
            if value == '':
                value = None
        return value

    @staticmethod
    def __validate_attribute__(attr) -> None:
        """
        Validate attribute to be set
        """
        if not isinstance(attr, str):
            raise ConfigurationError(f'Attribute is not string: {attr}')
        if not attr.isidentifier():
            raise ConfigurationError(f'Attribute is not valid python identifier: {attr}')
        if not RE_CONFIGURATIION_KEY.match(attr):
            raise ConfigurationError(f'Invalid attribute name: {attr}')

    def __format_attribute_value__(self, attr: str, value: Any) -> Any:
        """
        Format an attribute's value by attribute name
        """
        if attr in self.__float_settings__:
            return float(value)
        if attr in self.__integer_settings__:
            return int(value)
        if attr in self.__path_settings__:
            return Path(value).expanduser()

        validator_callback = getattr(self, f'validate_{attr}', None)
        if callable(validator_callback):
            try:
                value = validator_callback(value)  # pylint: disable=not-callable
            except Exception as error:
                raise ConfigurationError(f'Error validating setting {attr}: {error}') from error

        formatter_callback = getattr(self, f'format_{attr}', None)
        try:
            if callable(formatter_callback):
                value = formatter_callback(value)  # pylint: disable=not-callable
            else:
                value = self.default_formatter(value)
        except Exception as error:
            raise ConfigurationError(f'Error formatting setting {attr}: {error}') from error

        return value

    def as_dict(self) -> dict:
        """
        Return VS code configuration section as dictionary
        """
        data = {}
        for attribute in self.__attributes__:
            item = getattr(self, attribute)
            if hasattr(item, 'as_dict'):
                data[attribute] = item.as_dict()
            else:
                data[attribute] = item
        return data

    def set(self, attr: str, value: Any) -> None:
        """
        Load item with correct class
        """
        self.__validate_attribute__(attr)

        section = getattr(self, attr, None)
        if section is not None and callable(getattr(section, 'set', None)):
            section.set(attr, value)
            return

        if isinstance(value, dict):
            item = self.__dict_loader__(value, parent=self)  # pylint: disable=not-callable
            setattr(self, attr, item)
            self.__attributes__.append(attr)
            return

        if isinstance(value, (list, tuple)):
            item = self.__list_loader__(attr, value, parent=self)  # pylint: disable=not-callable
            setattr(self, item.__setting__, item)
            self.__attributes__.append(item.__setting__)
            return

        if value is not None:
            value = self.__format_attribute_value__(attr, value)

        setattr(self, attr, value)
        self.__attributes__.append(attr)


class ConfigurationList(ConfigurationItemContainer):
    """
    List of settings in configuration section
    """
    def __init__(self,
                 setting: Optional[Any] = None,
                 data: Optional[Any] = None,
                 parent: Optional[LoggingBaseClass] = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        super().__init__(parent=parent, debug_enabled=debug_enabled, silent=silent)
        self.__setting__ = setting
        self.__load__(data)

    def __repr__(self) -> str:
        return self.__values__.__repr__()

    def __getitem__(self, index: int) -> Any:
        return self.__values__[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.__values__.__setitem__(index, value)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.__values__)

    def __len__(self) -> int:
        return len(self.__values__)

    def __format_item__(self, value: Any) -> Any:
        """
        Format an item to be loaded to ConfigurationList

        By default returns original value. Override in child class as required.
        """
        return value

    def insert(self, index: int, value: Any) -> None:
        """
        Insert value to configuration list at specified index
        """
        self.__values__.insert(index, self.__format_item__(value))

    def append(self, value: Any) -> None:
        """
        Append value to configuration list
        """
        self.__values__.append(self.__format_item__(value))

    def __load__(self, value: Any) -> None:
        """
        Load list of values
        """
        self.__values__ = []
        if not value:
            return
        for item in value:
            if isinstance(item, dict):
                # pylint: disable=not-callable
                item = self.__dict_loader__(item, parent=self)
            self.append(item)

    def set(self, attr: str, value: Any) -> None:
        """
        Load value to list. Attribute is ignored in lists
        """
        self.__load__(value)


class ConfigurationSection(ConfigurationItemContainer):
    """
    Configuration section with validation

    Configuration sections can be nested and linked to parent configuration
    section by parent argument. If parent is given it must be an instance of
    ConfigurationSection.

    Any data given in data dictionary are inserted as settings.
    """
    __name__: str = None
    """Name of configuration section, used in linking custom classes"""
    __default_settings__: dict = {}
    """Dictionary of default settings configuration"""
    __required_settings__: Tuple[str] = ()
    """Tuple of settings required for valid configuration"""
    __environment_variables__: dict = {}
    """Mapping from environment variables read to settings"""
    __environment_variable_prefix__: Optional[str] = None
    """Prefix for reading settings from environment variables"""

    __section_loaders__: Tuple[Any] = ()
    """Classes used for subsection parsers"""
    __key_attribute_map__: dict = {}
    """Map configuration keys to python compatible attributes"""

    def __init__(self,
                 data: dict = dict,
                 parent: ConfigurationItemContainer = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        if parent is not None and not isinstance(parent, ConfigurationItemContainer):
            raise TypeError('parent must be instance of ConfigurationItemContainer')
        super().__init__(
            parent=parent,
            debug_enabled=debug_enabled,
            silent=silent,
        )

        self.__subsections__ = []

        self.__valid_settings__ = self.__detect_valid_settings__()
        for attr in self.__valid_settings__:
            self.set(attr, None)

        self.__initialize_sub_sections__()
        self.__load_dictionary__(self.__default_settings__)
        if isinstance(data, dict):
            self.__load_dictionary__(data)

        self.__load_environment_variables__()

        if parent is None:
            self.validate()

    def __repr__(self) -> str:
        return self.__name__ if self.__name__ is not None else ''

    def __initialize_sub_sections__(self) -> None:
        """
        Initialize sub sections configured in __section_loaders__
        """
        for loader in self.__section_loaders__:
            subsection = loader(
                data=None,
                parent=self,
                debug_enabled=self.__debug_enabled__,
                silent=self.__silent__
            )
            name = self.__attribute_from_key__(subsection.__name__)
            if name is None:
                raise ConfigurationError(f'Subsection class defines no name: {loader}')
            setattr(self, name, subsection)
            self.__attributes__.append(name)

    def __attribute_from_key__(self, key: str) -> Any:
        """
        Map settings key to python attribute
        """
        return self.__key_attribute_map__.get(key, key)

    def __key_from_attribute__(self, attr: str) -> Any:
        """
        Map settings file key from attribute
        """
        for key, value in self.__key_attribute_map__.items():
            if attr == value:
                return key
        return attr

    def __split_attribute_path__(self, key: str) -> Tuple[str, List[str]]:
        """
        Return section attribute from key
        """
        key = self.__attribute_from_key__(key)
        if isinstance(key, str):
            parts = key.split('.')
            return parts[0], '.'.join(parts[1:])
        return key, []

    def __detect_valid_settings__(self) -> List[str]:
        """
        Detect all known settings, return list of keys
        """
        attributes = []
        attributes = list(self.__required_settings__)
        for attr, value in self.__default_settings__.items():
            if not RE_CONFIGURATIION_KEY.match(attr):
                raise ConfigurationError(f'Invalid attribute name: {attr}')
            if not isinstance(value, dict) and attr not in attributes:
                attributes.append(attr)
        for attr in self.__environment_variables__.values():
            if not RE_CONFIGURATIION_KEY.match(attr):
                raise ConfigurationError(f'Invalid attribute name: {attr}')
            if attr not in attributes:
                attributes.append(attr)
        return sorted(set(attributes))

    def __load_environment_variables__(self) -> None:
        """
        Load settings from environment variables
        """
        if self.__environment_variable_prefix__ is not None:
            for attr in self.__valid_settings__:
                env = f'{self.__environment_variable_prefix__}_{attr}'.upper()
                value = os.environ.get(env, None)
                if value is not None:
                    self.set(attr, value)

        for env, attr in self.__environment_variables__.items():
            value = os.environ.get(env, None)
            if value is not None:
                self.set(attr, value)

    def __get_section_loader__(self, section_name: str) -> Any:
        """
        Find configuration section loader by name

        By default returns ConfigurationSection
        """
        if not isinstance(section_name, str) or section_name == '':
            raise ConfigurationError('Configuration section name not defined')

        section_name = self.__attribute_from_key__(section_name)
        for loader in self.__section_loaders__:
            loader_name = self.__attribute_from_key__(getattr(loader, '__name__', None))
            if loader_name == section_name:
                return loader
        return self.__dict_loader__

    def __get_or_create_subsection__(
            self,
            name: str,
            parent: Optional[LoggingBaseClass] = None) -> Any:
        if parent is None:
            parent = self
        if not hasattr(parent, name):
            loader = parent.__get_section_loader__(name)
            item = loader({}, parent=parent, debug_enabled=self.__debug_enabled__, silent=self.__silent__)
            item.__name__ = name
            setattr(parent, name, item)
            parent.__subsections__.append(item)
        return getattr(parent, name)

    def __init_subsection_path__(self, section_name: str, path: Path) -> Tuple[Any, str]:
        """
        Initialize subsections from config path

        Splits . separated path to config setting path, creates subsections
        on path excluding last component

        Returns subsection matching longest path and field (last path component).
        Field is not actually loaded as the dictionary key
        """
        subsection = self.__get_or_create_subsection__(section_name)
        path = path.split('.')
        field = path[-1]
        if len(path) > 1:
            for subsection_name in path[:-1]:
                subsection = self.__get_or_create_subsection__(
                    subsection_name,
                    parent=subsection
                )
        return subsection, field

    def __load_section__(self, section: str, data: Any, path: Optional[str] = None) -> None:
        """
        Load configuration section from data
        """
        if path is not None:
            subsection, item = self.__init_subsection_path__(section, path)
            if isinstance(data, dict):
                if item == path:
                    subsection = self.__get_or_create_subsection__(
                        item,
                        parent=subsection
                    )
                subsection.__load_dictionary__(data)
            else:
                subsection.set(item, data)
        elif isinstance(data, dict):
            subsection = self.__get_or_create_subsection__(section, parent=self)
            subsection.__load_dictionary__(data)
        else:
            raise ConfigurationError('not a dict')

    def __load_dictionary__(self, data: dict) -> None:
        """
        Load settings from dictionary

        Any dictionaries in data are loaded as child configuration sections
        """
        if not isinstance(data, dict):
            raise ConfigurationError(f'Dictionary is not dict instance: {data}')

        for key, value in data.items():
            attr, path = self.__split_attribute_path__(key)
            if path:
                self.__load_section__(attr, value, path)
            elif isinstance(value, dict):
                self.__load_section__(attr, value)
            else:
                self.set(key, value)

    def as_dict(self) -> dict:
        """
        Return configuration section as dictionary
        """
        data = super().as_dict()
        for subsection in self.__subsections__:
            data[subsection.__name__] = subsection.as_dict()
        return data

    def set(self, attr: str, value: Any) -> None:
        """
        Set configuration setting value as attribute of the object

        Attributes are set as ConfigurationItem classes by default.
        """
        attr, path = self.__split_attribute_path__(attr)
        if path:
            self.__load_section__(attr, value, path)
            return

        self.__validate_attribute__(attr)
        super().set(attr, value)

    def validate(self) -> None:
        """
        Validate loaded configuration settings

        Default implementation checks if required settings are set.
        """
        for attr in self.__required_settings__:
            value = getattr(self, attr, None)
            if value is None:
                raise ConfigurationError(f'{self} required setting {attr} has no value')
