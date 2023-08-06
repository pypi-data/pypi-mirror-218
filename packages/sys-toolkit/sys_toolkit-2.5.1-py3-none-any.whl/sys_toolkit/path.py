#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Cached lookup for executable commands in user PATH
"""
import os

from collections.abc import Collection
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Union

from .platform import detect_platform_family


class Executables(Collection):
    """
    Singleton instance containing of executable commands on user's PATH

    Initializes a collections.abc.Collection lookup cache for commands on PATH

    Cache can be looked up by command name or with .get() method
    """
    __platform_family__: str = None
    """OS Platform family"""
    __path__: str = None
    """Path value being inspected"""
    __executables__: List[Path] = []
    """List of all executables detected on path, including duplicate commands"""
    __commands__: Dict = None
    """List of active commands on path"""

    def __init__(self):
        self.__platform_family__ = detect_platform_family()
        if Executables.__commands__ is None:
            Executables.__commands__ = Executables.__load__executables_on_path__(self)

    def __repr__(self) -> str:
        return self.__path__

    def __contains__(self, item: Union[str, Path]) -> bool:
        return item in self.__executables__ or item in self.__commands__

    def __iter__(self) -> Iterator[str]:
        return iter(self.__commands__.values())

    def __len__(self) -> int:
        return len(list(self.__commands__.keys()))

    def __getitem__(self, index: str) -> str:
        return self.__commands__[index]

    def __load__executables_on_path__(self) -> List[Path]:
        """
        Load executables available on user path
        """
        self.__executables__ = []
        commands = {}
        self.__path__ = os.environ.get('PATH', '')
        for path in self.__path__.split(os.pathsep):
            directory = Path(path)
            if not directory.is_dir():
                continue
            for filename in directory.iterdir():
                command = directory.joinpath(filename)
                try:
                    if not command.is_file():
                        continue
                    if self.__platform_family__ != 'windows':
                        if not os.access(command, os.X_OK):
                            continue
                except OSError:
                    continue
                self.__executables__.append(command)
                if filename.name not in commands:
                    commands[filename.name] = command
        return commands

    def paths(self, name: str) -> List[Path]:
        """
        Return all detected paths for command with specific name
        """
        return [
            item
            for item in self.__executables__
            if item.name == name
        ]

    def get(self, name: str) -> Optional[Path]:
        """
        Get path to command by name

        Return pathlib.Path reference to the command
        Returns None if command is not found
        """
        try:
            return self[name]
        except KeyError:
            return None
