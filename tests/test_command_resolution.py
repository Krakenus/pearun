from tempfile import NamedTemporaryFile
from unittest import TestCase, mock

from pearun.exceptions import PearunException
from pearun.parser import get_command
from pearun.pearunfile import Pearunfile


class CommandResolutionTestCase(TestCase):

    def setUp(self):
        self.commands_json = '''{
            "command_a": "echo 'A'",
            "command_b": "./deploy.sh"
        }'''

    @mock.patch('sys.argv', ['pearun', 'command_c'])
    def test_unexisting_command(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            with self.assertRaisesRegex(PearunException, r'Unrecognized command.*'):
                pearunfile = Pearunfile(temp_file.name)
                get_command(pearunfile)

    def test_known_command(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            command_name = 'command_a'
            with mock.patch('sys.argv', ['pearun', command_name]):
                pearunfile = Pearunfile(temp_file.name)
                command = get_command(pearunfile)
        self.assertEqual(command, pearunfile[command_name])

    def test_command_with_args(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            command_name = 'command_b'
            command_args = ['production', 'fast']
            sys_argv = ['pearun', command_name] + command_args
            pearunfile = Pearunfile(temp_file.name)
            expected_command = ' '.join([pearunfile[command_name]] + command_args)

            with mock.patch('sys.argv', sys_argv):
                command = get_command(pearunfile)
        self.assertEqual(command, expected_command)
