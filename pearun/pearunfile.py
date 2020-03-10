import json
from collections import OrderedDict

from pearun.exceptions import PearunfileException


class Pearunfile:

    def __init__(self, path: str):
        self.path = path
        self._commands = None

    def _parse_commands(self):
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
    def commands(self):
        if not self._commands:
            self._commands = self._parse_commands()
        return self._commands

    def __getitem__(self, item):
        return self.commands[item]

    def __contains__(self, item):
        return item in self.commands
