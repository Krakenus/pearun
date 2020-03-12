import sys
import subprocess
import os

import click

from pearun.exceptions import PearunException, UnspecifiedCommandException, PearunfileException
from pearun.pearunfile import Pearunfile

__all__ = ['main']


def _execute_command(command, cwd) -> None:
    """
    Runs specified command
    :param command: command to run
    :param cwd: dir containing Pearunfile for cwd change so relative paths from Pearunfile are valid
    """
    os.chdir(cwd)
    process = subprocess.Popen(command, shell=True)
    process.wait()


def _show_help() -> None:
    with click.Context(main) as context:
        help = context.get_help()
        print(help)


def _list_commands(pearunfile: Pearunfile) -> None:
    if len(pearunfile):
        print('Available commands:')
        for command_name, command in pearunfile.commands.items():
            print('    {:<20}{:<40}'.format(command_name, command))


def _show_help_and_list_commands(pearunfile: Pearunfile) -> None:
    _show_help()
    print('')
    _list_commands(pearunfile)


@click.command(help='Tool for running user defined scripts')
@click.option(
    '-h',
    '--help',
    default=False,
    is_flag=True,
    help='Show this message and exit'
)
@click.option(
    '-f',
    '--file',
    default='Pearunfile',
    show_default=True,
    envvar='PEARUNFILE',
    type=click.Path(),
    help='Specify Pearunfile path'
)
@click.option(
    '-l',
    '--list',
    default=False,
    is_flag=True,
    help='List available commands'
)
@click.argument(
    'command',
    type=click.STRING,
    required=False
)
@click.argument(
    'args',
    nargs=-1,
    type=click.STRING
)
def main(**kwargs):
    if kwargs.get('help', False):
        _show_help()
        sys.exit(0)

    file_path = kwargs.get('file')

    try:
        pearunfile = Pearunfile(file_path)
    except PearunException as e:
        print(e, end='\n\n')
        _show_help()
        sys.exit(1)
    except PearunfileException as e:
        print(e)
        sys.exit(1)

    if kwargs.get('list', False):
        _list_commands(pearunfile)
        sys.exit(0)

    command_name = kwargs.get('command')
    args = kwargs.get('args', [])

    try:
        command = pearunfile.resolve_command(command_name, *args)
    except UnspecifiedCommandException:
        _show_help_and_list_commands(pearunfile)
        sys.exit(1)
    except PearunException as e:
        print(e, end='\n\n')
        _list_commands(pearunfile)
        sys.exit(1)

    cwd = os.path.dirname(file_path)
    _execute_command(command, cwd)


if __name__ == '__main__':
    main()
