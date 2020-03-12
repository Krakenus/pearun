import unittest
from tempfile import NamedTemporaryFile

from pearun.pearunfile import Pearunfile
from pearun.exceptions import PearunfileException


class PearunfileTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_json = '{"aaa": "bb", "foo": "bar"}'
        self.invalid_json = '{"aaa": aaa}'
        self.non_string_json = '{"aaa": 123}'
        self.complex_json = '{"aaa": [1, 2, 3]}'

    def test_invalid_json(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.invalid_json)
            temp_file.flush()

            with self.assertRaisesRegex(PearunfileException, r'Pearunfile parsing failed.*'):
                Pearunfile(temp_file.name)

    def test_non_string_commands(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.non_string_json)
            temp_file.flush()

            with self.assertRaisesRegex(PearunfileException, r'Pearunfile validation failed.*'):
                Pearunfile(temp_file.name)

    def test_complex_json(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.complex_json)
            temp_file.flush()

            with self.assertRaisesRegex(PearunfileException, r'.*commands are not string values$'):
                Pearunfile(temp_file.name)

    def test_valid_json(self):
        with NamedTemporaryFile(mode='w') as temp_file:
            temp_file.write(self.valid_json)
            temp_file.flush()

            pearunfile = Pearunfile(temp_file.name)
            self.assertDictEqual(pearunfile.commands, {
                'aaa': 'bb',
                'foo': 'bar',
            })
