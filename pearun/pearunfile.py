from collections import OrderedDict
import json
import typing
import os

from pearun.exceptions import PearunfileException, PearunException


class Pearunfile:

    def __init__(self, path: str):
        self.path: str = path
        self._commands: typing.Optional[OrderedDict] = None
        self._check_file_exists()

    def _check_file_exists(self):
        if not os.path.exists(self.path):
            raise PearunException('File {} not exists'.format(self.path))

    def _parse_commands(self) -> OrderedDict:
        """
        parses a json Pearunfile to dict and makes it sorted
        :param file_path:
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
        if not self._commands:
            self._commands = self._parse_commands()
        return self._commands

    def __getitem__(self, item: str) -> str:
        return self.commands[item]

    def __contains__(self, item: str) -> bool:
        return item in self.commands
