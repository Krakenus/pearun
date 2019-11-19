from collections import OrderedDict
import argparse
import json
import os

from pearun.exceptions import PearunException, UnspecifiedCommandException, PearunfileException

DEFAULT_JSON = 'Pearunfile'


class CommandAction(argparse._StoreAction):
    """
    Action to store available commands
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.choices is None:
            self.choices = []
        self._choices_actions = []

    def add_choice(self, choice, help_text=''):
        self.choices.append(choice)
        command_action = argparse.Action(option_strings=[], dest=choice, help=help_text)
        self._choices_actions.append(command_action)

    def _get_subactions(self):
        return self._choices_actions


def _get_base_parser(add_help=False):
    """
    :param add_help
    :return ArgumentParser instance with default arguments added
    """
    parser = argparse.ArgumentParser(description='Tool for running user defined scripts', add_help=add_help)
    parser.add_argument('-f', '--file', help='Specify Pearunfile path')
    return parser


def get_file_path():
    """
    :return: path to Pearunfile to be parsed
    """
    parser = _get_base_parser()
    args, _ = parser.parse_known_args()
    file_path = args.file if args and args.file else DEFAULT_JSON
    if not os.path.exists(file_path):
        raise PearunException('File {} not exists'.format(file_path), parser=parser)
    file_path = os.path.abspath(file_path)
    return file_path


def parse_commands(file_path):
    """
    parses a json Pearunfile to dict and makes it sorted
    :param file_path:
    :return: OrderedDict of defined commands
    """
    with open(file_path) as file:
        try:
            commands = json.load(file)
        except Exception as e:
            raise PearunfileException('Pearunfile parsing failed: {}'.format(e))
    if not all(isinstance(command, str) for command in commands.values()):
        raise PearunfileException('Pearunfile validation failed: commands are not string values')
    return OrderedDict(sorted(commands.items()))


def get_command(commands):
    """
    :param commands: dict of available commands
    :return: parsed command name defined in Pearunfile
    """
    parser = _get_base_parser(add_help=True)
    parser.register('action', 'store_command', CommandAction)

    group = parser.add_argument_group(title='Available commands')
    command_choices = group.add_argument('command', nargs='...', metavar='COMMAND', action='store_command')
    for command_name, script in commands.items():
        command_choices.add_choice(command_name, help_text=script)

    args, unknown_args = parser.parse_known_args()
    command = args.command

    if not command:
        raise UnspecifiedCommandException(parser=parser)

    try:
        command[0] = commands[command[0]]
    except KeyError:
        raise PearunException('Unrecognized command: {}'.format(command[0]), parser=parser)

    if len(command) > 1:
        command = ' '.join(command)

    return command
