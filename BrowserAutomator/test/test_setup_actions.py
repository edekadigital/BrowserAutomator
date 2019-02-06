from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.setup_actions import *
from BrowserAutomator.test.mocks import SeleniumMock


class SetupActionsTest(TestCase):
    filename = "filename"
    url_0 = "https://testsite_0.com"
    url_1 = "https://testsite_1.com"
    all_actions = {"wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs, "interact": interact,
                   "for every": for_every}
    driver = SeleniumMock()
    actions = [(lambda driver, content: None, "a"), (lambda driver, content: 1, "b")]

    @patch("BrowserAutomator.setup_actions.get_actions", side_effect=lambda filename, all_actions: True)
    def test_actions_from_file(self, get_actions_mock):
        result = actions_from_file(self.filename)
        self.assertTrue(result)
        get_actions_mock.assert_called_with(self.filename, self.all_actions)

    @patch("BrowserAutomator.setup_actions.get_action_functions", side_effect=lambda variables, all_actions: True)
    def test_actions_from_variable(self, get_action_functions_mock):
        result = actions_from_variable("variables")
        self.assertTrue(result)
        get_action_functions_mock.assert_called_with("variables", self.all_actions)

    def test_run_functions(self):
        result = run_functions(self.driver, self.actions[:1])
        self.assertIsNone(result)
        result = run_functions(self.driver, self.actions[1:])
        self.assertEqual(1, result)

    @patch("BrowserAutomator.setup_actions.actions_from_file", side_effect=lambda filename: [(lambda driver, content: None, "a")])
    def test_action_runner_good(self, actions_from_file_mock):
        result = action_runner(self.driver, self.filename)
        self.assertEqual(None, result)
        actions_from_file_mock.assert_called_with(self.filename)

    @patch("BrowserAutomator.setup_actions.actions_from_file", side_effect=lambda filename: [(lambda driver, content: 1, "a")])
    def test_action_runner_bad(self, actions_from_file_mock):
        result = action_runner(self.driver, self.filename)
        self.assertEqual(1, result)
        actions_from_file_mock.assert_called_with(self.filename)

    @patch("BrowserAutomator.setup_actions.sleep")
    def test_wait(self, sleep_mock):
        content = [{"days": 1}]
        wait(self.driver, content)
        sleep_mock.assert_called_with(1*24*60*60)

    def test_load_url(self):
        """given a url as `content`, opens the url"""
        load_url(self.driver, self.url_0)
        self.assertEqual(self.url_0, self.driver.url)

    @patch("BrowserAutomator.setup_actions.load_url", side_effect=lambda driver, content: 0)
    def test_new_tab(self, load_url_mock):
        # testing exception
        self.driver.throw_js_error = True
        result = new_tab(self.driver, self.url_0)
        self.assertEqual(1, result)
        # testing normally
        self.driver.throw_js_error = False
        result = new_tab(self.driver, self.url_0)
        self.assertEqual(0, result)
        load_url_mock.assert_called_with(self.driver, self.url_0)
        self.assertEqual(1, self.driver.switch_to.current_window)

    def test_switch_tabs(self):
        self.driver.switch_to.throw_window_error = True
        result = switch_tabs(self.driver, 0)
        self.assertEqual(1, result)
        self.driver.switch_to.throw_window_error = False
        result = switch_tabs(self.driver, 0)
        self.assertEqual(None, result)
        self.assertEqual(0, self.driver.switch_to.current_window)

    @patch("BrowserAutomator.setup_actions.action_on_element")
    def test_interact(self, action_on_element_mock):
        content = [{"type": 1, "name": 2, "content": 3}, {"type": 4, "name": 5}]
        result = interact(self.driver, content)
        self.assertEqual(None, result)
        call_args = action_on_element_mock.call_args_list
        self.assertEqual((self.driver, 1, 2, 3), list(call_args[0])[0])
        self.assertEqual((self.driver, 4, 5, None), list(call_args[1])[0])

    def test_action_on_element(self):
        # TODO
        pass

    @patch("BrowserAutomator.setup_actions.actions_from_variable", side_effect=lambda actions: actions)
    @patch("BrowserAutomator.setup_actions.run_functions", side_effect=lambda driver, functions: 0)
    def test_for_every(self, run_functions_mock, actions_from_variable_mock):
        # TODO
        content = {"urls": [self.url_0, self.url_1],
                   "actions": [
                       {"load": ""}
                   ]}
        result = for_every(self.driver, content)
        # self.assertEqual(None, result)
        # print(run_functions_mock.call_args_list)


if __name__ == '__main__':
    main()
