import os
import sys
import subprocess

import click

from pearun.exceptions import PearunException, UnspecifiedCommandException, PearunfileException
from pearun.parser import get_file_path, get_command
from pearun.pearunfile import Pearunfile

__all__ = ['main']


def _execute_command(command, cwd):
    """
    Runs specified command
    :param command: command to run
    :param cwd: dir containing Pearunfile for cwd change so relative paths from Pearunfile are valid
    """
    os.chdir(cwd)
    process = subprocess.Popen(command, shell=True)
    process.wait()


def _show_help():
    with click.Context(main) as context:
        help = context.get_help()
        print(help)


def _validate_pearun_file(file_path):
    if not os.path.exists(file_path):
        raise PearunException('File {} not exists'.format(file_path))


def _list_commands(commands: dict):
    if commands:
        print('Available commands:')
        for command_name, command in commands.items():
            print('    {:<20}{:<40}'.format(command_name, command))


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

    commands = {}
    try:
        file_path = kwargs.get('file')
        _validate_pearun_file(file_path)
        pearunfile = Pearunfile(file_path)

        if kwargs.get('list', False):
            _list_commands(commands)
            sys.exit(0)

        cmd = get_command(pearunfile)
    except UnspecifiedCommandException:
        _show_help()
        print('')
        _list_commands(commands)
        sys.exit(1)
    except PearunException as e:
        print(e, end='\n\n')
        _show_help()
        sys.exit(1)
    except PearunfileException as e:
        print(e)
        sys.exit(1)
    else:
        cwd = os.path.dirname(file_path)
        _execute_command(cmd, cwd)


if __name__ == '__main__':
    main()
