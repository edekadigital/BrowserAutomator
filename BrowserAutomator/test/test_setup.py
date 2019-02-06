from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.setup import setup
from BrowserAutomator.test.mocks import SeleniumMock


class RunnerTest(TestCase):
    setup_file, loop_file = "setup_file", "loop_file"

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 0)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 0)
    def test_setup_good(self, selenium_setup_mock, action_runner_mock, loop_runner_mock):
        result = setup(self.setup_file, self.loop_file)
        self.assertEqual(0, result)
        self.assertTrue(SeleniumMock().quit_called)

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 1)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 0)
    def test_setup_bad_action_runner(self, selenium_setup_mock, action_runner_mock, loop_runner_mock):
        result = setup(self.setup_file, self.loop_file)
        self.assertEqual(1, result)
        self.assertTrue(SeleniumMock().quit_called)

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 0)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 1)
    def test_setup_bad_loop_runner(self, selenium_setup_mock, action_runner_mock, loop_runner_mock):
        result = setup(self.setup_file, self.loop_file)
        self.assertEqual(1, result)
        self.assertTrue(SeleniumMock().quit_called)


if __name__ == '__main__':
    main()
