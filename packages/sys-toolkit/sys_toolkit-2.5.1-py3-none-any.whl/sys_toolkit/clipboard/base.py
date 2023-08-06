#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base class for clipboards
"""
import os

from subprocess import run, CalledProcessError, CompletedProcess, PIPE
from typing import List, Tuple

from ..constants import DEFAULT_ENCODING
from ..exceptions import ClipboardError
from ..path import Executables
from ..modules import check_available_imports

CLIPBOARD_LOCALE = 'en_US.UTF-8'


class ClipboardBaseClass:
    """
    Base class implementation of clipboard copy and paste functions
    """
    __required_commands__: Tuple[str] = ()
    __required_env__: Tuple[str] = ()
    __required_modules__: Tuple[str] = ()

    def __check_required_modules__(self) -> bool:
        """
        Check if required python modules are available

        Returns true if no required modules are defined in __required_modules__
        """
        return check_available_imports(*self.__required_modules__)

    def __check_required_env__(self) -> bool:
        """
        Check required environment variables are defined and have non-empty value
        """
        for var in self.__required_env__:
            if not os.environ.get(var, None):
                return False
        return True

    def __check_required_cli_commands__(self) -> bool:
        """
        Check if required CLI commands are available
        """
        if not self.__required_commands__:
            return False
        executables = Executables()
        for command in self.__required_commands__:
            if command not in executables:
                return False
        return True

    def __run_command__(self, *command) -> None:
        """
        Run generic CLI commands without stdin
        """
        try:
            run(*command, check=True, env=self.env)
        except CalledProcessError as error:
            cmd = ' '.join(command)
            raise ClipboardError(f'Error running command "{cmd}": {error}') from error

    def __copy_command_stdin__(self, data, *command: List[str]) -> None:
        """
        Generic implementation to copy data from clipboard with specified CLI commmand
        and data from stdin to the command
        """
        data = str(data).rstrip('\n')
        try:
            run(*command, input=data.encode(), check=True, env=self.env)
        except CalledProcessError as error:
            raise ClipboardError(f'Error copying text to clipboard: {error}') from error

    def __paste_command_stdout__(self, *command: List[str]) -> str:
        """
        Generic implementation to paste data from stdout of specified CLI command
        """
        try:
            res = run(*command, stdout=PIPE, stderr=PIPE, check=False, env=self.env)
            if res.returncode == 0:
                return str(res.stdout, encoding=DEFAULT_ENCODING)
            return self.__process_paste_error__(res)
        except CalledProcessError as error:
            raise ClipboardError(f'Error pasting text from clipboard: {error}') from error

    def __process_paste_error__(self, response: CompletedProcess):
        """
        Process return value for paste command error

        By default just raises Clipboard Error
        """
        raise ClipboardError(
            f'Error pasting text from clipboard: command returns code {response.returncode}'
        )

    @property
    def env(self) -> dict:
        """
        Environment variables for commands
        """
        env = os.environ.copy()
        env['LANG'] = CLIPBOARD_LOCALE
        return env

    @property
    def available(self) -> bool:
        """
        Property to check if this type of clipboard is available

        Override in parent class with actual test. By default returns False
        """
        return False

    def clear(self) -> None:
        """
        Clear data on clipboard
        """
        raise NotImplementedError('Clipboard clear() must be implemented in child class')

    def copy(self, data: str):
        """
        Copy data to clipboard
        """
        raise NotImplementedError('Clipboard copy() must be implemented in child class')

    def paste(self) -> str:
        """
        Get data from clipboard
        """
        raise NotImplementedError('Clipboard paste() must be implemented in child class')
