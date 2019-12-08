from unittest import TestCase
from unittest.mock import patch

from pearun.exceptions import PearunException
from pearun.parser import get_command


class CommandResolutionTestCase(TestCase):

    def setUp(self):
        self.commands = {
            'command_a': 'echo "A"',
            'command_b': './deploy.sh',
        }

    @patch('sys.argv', ['pearun', 'command_c'])
    def test_unexisting_command(self):
        with self.assertRaisesRegex(PearunException, r'Unrecognized command.*'):
            get_command(self.commands)

    def test_known_command(self):
        command_name = 'command_a'
        with patch('sys.argv', ['pearun', command_name]):
            command = get_command(self.commands)
        self.assertEqual(command, self.commands[command_name])

    def test_command_with_args(self):
        command_name = 'command_b'
        command_args = ['production', 'fast']
        sys_argv = ['pearun', command_name] + command_args
        expected_command = ' '.join([self.commands[command_name]] + command_args)

        with patch('sys.argv', sys_argv):
            command = get_command(self.commands)
        self.assertEqual(command, expected_command)
