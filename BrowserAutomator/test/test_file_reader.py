from unittest import TestCase, main
from unittest.mock import patch
from pathlib import Path
from BrowserAutomator.file_reader import read_actions
from BrowserAutomator.test.mocks import YamlMock



class FileReaderTest(TestCase):
    @patch("BrowserAutomator.file_reader.YAML", side_effect=YamlMock)
    def test_read_actions(self, yaml_mock: patch):
        expected_filename = "expected_filename"
        result = read_actions(expected_filename)
        self.assertEqual(Path(expected_filename), result)
        yaml_mock.assert_called_with(typ="safe")


if __name__ == '__main__':
    main()
