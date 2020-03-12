import json
from tempfile import NamedTemporaryFile
from unittest import TestCase

from pearun.exceptions import PearunException
from pearun.pearunfile import Pearunfile


class CommandResolutionTestCase(TestCase):

    def setUp(self):
        self.commands = {
            'command_a': 'echo "A"',
            'command_b': './deploy.sh',
        }
        self.commands_json = json.dumps(self.commands)

    def test_unexisting_command(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            with self.assertRaisesRegex(PearunException, r'Unrecognized command.*'):
                pearunfile = Pearunfile(temp_file.name)
                pearunfile.resolve_command('command_c')

    def test_known_command(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            command_name = 'command_a'
            pearunfile = Pearunfile(temp_file.name)
            command = pearunfile.resolve_command(command_name)
        self.assertEqual(command, pearunfile[command_name])
        self.assertEqual(command, self.commands[command_name])

    def test_command_with_args(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.commands_json)
            temp_file.flush()

            command_name = 'command_b'
            command_args = ['production', '--fast']
            pearunfile = Pearunfile(temp_file.name)
            expected_command = ' '.join([self.commands[command_name]] + command_args)

            command = pearunfile.resolve_command(command_name, *command_args)
        self.assertEqual(command, expected_command)
