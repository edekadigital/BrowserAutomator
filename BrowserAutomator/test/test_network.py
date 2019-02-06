from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.network import check_network_not_working
from BrowserAutomator.test.mocks import RequestMock


class NetworkTest(TestCase):
    network_test_url = "https://www.google.com"

    @patch("BrowserAutomator.network.get", side_effect=lambda url: RequestMock())
    def test_good_request(self, get_mock):
        result = check_network_not_working()
        self.assertFalse(result)
        get_mock.assert_called_with(self.network_test_url)

    @patch("BrowserAutomator.network.get", side_effect=lambda url: RequestMock(test_redirect=True))
    def test_redirect_request(self, get_mock):
        result = check_network_not_working()
        self.assertTrue(result)
        get_mock.assert_called_with(self.network_test_url)

    @patch("BrowserAutomator.network.get", side_effect=lambda url: RequestMock(raise_error=True))
    def test_error_request(self, get_mock):
        try:
            result = check_network_not_working()
        except ConnectionError:
            result = False
        self.assertTrue(result)
        get_mock.assert_called_with(self.network_test_url)


if __name__ == '__main__':
    main()
