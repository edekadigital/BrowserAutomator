from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.selenium_setup import selenium_setup
from BrowserAutomator.test.mocks import SeleniumMock, ChromeOptions


class SeleniumSetupTest(TestCase):
    setup_file, loop_file = "setup_file", "loop_file"
    chrome_options = ChromeOptions()

    @patch("BrowserAutomator.selenium_setup.ChromeOptions", side_effect=lambda: ChromeOptions())
    @patch("BrowserAutomator.selenium_setup.Chrome", side_effect=SeleniumMock)
    def test_selenim_setup(self, selenium_mock, chrome_options_mock):
        result = selenium_setup()
        chrome_options_mock.assert_called_once()
        self.assertEqual("/usr/lib/chromium-browser/chromedriver", selenium_mock.call_args[0][0])
        self.assertEqual(type(ChromeOptions()), type(selenium_mock.call_args[1]["chrome_options"]))
        self.assertEqual(type(SeleniumMock()), type(result))
        self.assertTrue(SeleniumMock().fullscreen)


if __name__ == '__main__':
    main()
