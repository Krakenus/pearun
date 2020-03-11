from collections import OrderedDict
import json
import typing
import os

from pearun.exceptions import PearunfileException, PearunException, UnspecifiedCommandException


class Pearunfile:

    def __init__(self, path: str, lazy: bool = False):
        self.path: str = path
        self._check_file_exists()
        self._commands: typing.Optional[OrderedDict] = None if lazy else self._parse_commands()

    def _check_file_exists(self) -> None:
        if not os.path.exists(self.path):
            raise PearunException('File {} not exists'.format(self.path))

    def _parse_commands(self) -> OrderedDict:
        """
        parses a json Pearunfile to dict and makes it sorted
        :return: OrderedDict of defined commands
        """
        with open(self.path) as file:
            try:
                commands = json.load(file)
            except Exception as e:
                raise PearunfileException('Pearunfile parsing failed: {}'.format(e))
        if not all(isinstance(command, str) for command in commands.values()):
            raise PearunfileException('Pearunfile validation failed: commands are not string values')
        return OrderedDict(sorted(commands.items()))

    @property
    def commands(self) -> OrderedDict:
        """
        :return:
        """
        if not self._commands:
            self._commands = self._parse_commands()
        return self._commands

    def resolve_command(self, command_name: str, *args) -> str:
        """
        :param command_name:
        :param args:
        :return:
        """

        if not command_name:
            raise UnspecifiedCommandException()

        try:
            command = self[command_name]
        except KeyError:
            raise PearunException('Unrecognized command: {}'.format(command_name))
        command = ' '.join([command, *args])
        return command

    def __bool__(self) -> bool:
        return bool(self.commands)

    def __len__(self) -> int:
        return len(self.commands)

    def __getitem__(self, item: str) -> str:
        return self.commands[item]

    def __contains__(self, item: str) -> bool:
        return item in self.commands
