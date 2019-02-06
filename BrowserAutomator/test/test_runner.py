from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.runner import get_actions, get_action_functions


class RunnerTest(TestCase):
    @patch("BrowserAutomator.runner.read_actions", side_effect=lambda filename: ["action_0"])
    @patch("BrowserAutomator.runner.get_action_functions", side_effect=lambda actions, types: ["parsed_action_0"])
    def test_get_actions(self, get_action_functions_mock, read_actions_mock):
        expected_filename = "expected_filename"
        result = get_actions(expected_filename, {0: 1})
        self.assertEqual(result, ["parsed_action_0"])
        read_actions_mock.assert_called_with(expected_filename)
        get_action_functions_mock.assert_called_with(["action_0"], {0: 1})

    def test_get_action_functions(self):
        actions = [{"0": "content0"}, {"1": "content1"}, {"2": "content2"}]
        types = {"0": 0, "1": 1, "2": 2}
        result = get_action_functions(actions, types)
        self.assertEqual(result, [(0, "content0"), (1, "content1"), (2, "content2")])


if __name__ == '__main__':
    main()
