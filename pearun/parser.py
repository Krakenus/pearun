import argparse
import os

from pearun.exceptions import PearunException, UnspecifiedCommandException
from pearun.pearunfile import Pearunfile

DEFAULT_JSON = 'Pearunfile'


class CommandAction(argparse.Action):
    """
    Action to store available commands
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.choices is None:
            self.choices = []
        self._choices_actions = []

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

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
        raise PearunException('File {} not exists'.format(file_path))
    file_path = os.path.abspath(file_path)
    return file_path


def get_command(pearunfile: Pearunfile) -> str:
    """
    :param pearunfile: Pearunfile instance
    :return: parsed command name defined in Pearunfile
    """
    parser = _get_base_parser(add_help=True)
    parser.register('action', 'store_command', CommandAction)

    group = parser.add_argument_group(title='Available commands')
    command_choices = group.add_argument('command', nargs='...', metavar='COMMAND', action='store_command')
    for command_name, script in pearunfile.commands.items():
        command_choices.add_choice(command_name, help_text=script)

    args, unknown_args = parser.parse_known_args()
    command = args.command

    if not command:
        raise UnspecifiedCommandException()

    try:
        command[0] = pearunfile.commands[command[0]]
    except KeyError:
        raise PearunException('Unrecognized command: {}'.format(command[0]))

    command = ' '.join(command)

    return command
