import os
import subprocess

from pearun.exceptions import PearunException, UnspecifiedCommandException, PearunfileException
from pearun.parser import get_file_path, parse_commands, get_command

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


def main():
    try:
        file = get_file_path()
        commands = parse_commands(file)
        command = get_command(commands)
    except UnspecifiedCommandException as e:
        e.print_help()
    except PearunException as e:
        print(e, end='\n\n')
        e.print_help()
    except PearunfileException as e:
        print(e)
    else:
        cwd = os.path.dirname(file)
        _execute_command(command, cwd)


if __name__ == '__main__':
    main()
