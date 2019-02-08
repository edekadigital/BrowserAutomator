from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.setup import setup, setup_caller
from BrowserAutomator.test.mocks import SeleniumMock


class SetupTest(TestCase):
    setup_files, loop_files, chromedriver_path = ["setup_file"], ["loop_file"], "path"
    driver = SeleniumMock()

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 0)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 0)
    def test_setup_good(self, loop_runner_mock, action_runner_mock, selenium_setup_mock):
        result = setup(self.setup_files, self.loop_files, self.chromedriver_path)
        self.assertEqual(0, result)
        self.assertTrue(SeleniumMock().quit_called)
        selenium_setup_mock.assert_called_with(self.chromedriver_path)
        action_runner_mock.assert_called_with(self.driver, self.setup_files)
        loop_runner_mock.assert_called_with(self.driver, self.loop_files, self.setup_files)

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 1)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 0)
    def test_setup_bad_action_runner(self, loop_runner_mock, action_runner_mock, selenium_setup_mock):
        result = setup(self.setup_files, self.loop_files, self.chromedriver_path)
        self.assertEqual(1, result)
        self.assertTrue(SeleniumMock().quit_called)
        selenium_setup_mock.assert_called_with(self.chromedriver_path)
        action_runner_mock.assert_called_with(self.driver, self.setup_files)
        loop_runner_mock.assert_not_called()

    @patch("BrowserAutomator.setup.selenium_setup", side_effect=SeleniumMock)
    @patch("BrowserAutomator.setup.action_runner", side_effect=lambda driver, filename=None: 0)
    @patch("BrowserAutomator.setup.loop_runner", side_effect=lambda driver, filename=None, setup_filename=None: 1)
    def test_setup_bad_loop_runner(self, loop_runner_mock, action_runner_mock, selenium_setup_mock):
        result = setup(self.setup_files, self.loop_files, self.chromedriver_path)
        self.assertEqual(1, result)
        self.assertTrue(SeleniumMock().quit_called)
        selenium_setup_mock.assert_called_with(self.chromedriver_path)
        action_runner_mock.assert_called_with(self.driver, self.setup_files)
        loop_runner_mock.assert_called_with(self.driver, self.loop_files, self.setup_files)

    @patch("BrowserAutomator.setup.sleep")
    @patch("BrowserAutomator.setup.setup")
    def test_setup_caller(self, setup_mock, sleep_mock):
        setup_caller(self.setup_files, self.loop_files, self.chromedriver_path)
        setup_mock.assert_called_with(self.setup_files, self.loop_files, self.chromedriver_path)
        sleep_mock.assert_called_with(30)


if __name__ == '__main__':
    main()
