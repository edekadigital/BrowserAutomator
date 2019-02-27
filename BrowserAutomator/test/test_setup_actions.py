from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.setup_actions import *
from BrowserAutomator.test.mocks import SeleniumMock
from BrowserAutomator.test import mocks
from BrowserAutomator import setup_actions


class SetupActionsTest(TestCase):
    filenames = ["filename"]
    url_0 = "https://testsite_0.com"
    url_1 = "https://testsite_1.com"
    all_actions = {"zoom": zoom,"wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs, "interact": interact,
                   "for every": for_every}
    driver = SeleniumMock()
    actions = [(lambda driver, content: None, "a"), (lambda driver, content: 1, "b")]

    @patch("BrowserAutomator.setup_actions.get_actions", side_effect=lambda filename, all_actions: True)
    def test_actions_from_file(self, get_actions_mock):
        result = actions_from_file(self.filenames)
        self.assertTrue(result)
        get_actions_mock.assert_called_with(self.filenames, self.all_actions)

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

    @patch("BrowserAutomator.setup_actions.actions_from_file",
           side_effect=lambda filename: [(lambda driver, content: None, "a")])
    def test_action_runner_good(self, actions_from_file_mock):
        # testing list of filenames
        result = action_runner(self.driver, self.filenames)
        self.assertEqual(None, result)
        actions_from_file_mock.assert_called_with(self.filenames[0])
        # testing string for filename
        result = action_runner(self.driver, self.filenames[0])
        self.assertEqual(None, result)
        actions_from_file_mock.assert_called_with(self.filenames[0])

    @patch("BrowserAutomator.setup_actions.actions_from_file",
           side_effect=lambda filename: [(lambda driver, content: 1, "a")])
    def test_action_runner_bad(self, actions_from_file_mock):
        result = action_runner(self.driver, self.filenames)
        self.assertEqual(1, result)
        actions_from_file_mock.assert_called_with(self.filenames[0])

    def test_zoom(self):
        zoom(self.driver, "50%")
        self.assertEqual("document.body.style.zoom = '50%';", self.driver.last_script)

    @patch("BrowserAutomator.setup_actions.sleep")
    def test_wait(self, sleep_mock):
        content = [{"days": 1}]
        wait(self.driver, content)
        sleep_mock.assert_called_with(1 * 24 * 60 * 60)

    def test_load_url(self):
        """given a url as `content`, opens the url"""
        load_url(self.driver, self.url_0)
        self.assertEqual(self.url_0, self.driver.url)
        self.driver.reset()

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
        self.driver.reset()

    def test_switch_tabs(self):
        self.driver.switch_to.throw_window_error = True
        result = switch_tabs(self.driver, 0)
        self.assertEqual(1, result)
        self.driver.switch_to.throw_window_error = False
        result = switch_tabs(self.driver, 0)
        self.assertEqual(None, result)
        self.assertEqual(0, self.driver.switch_to.current_window)
        self.driver.reset()

    @patch("BrowserAutomator.setup_actions.action_on_element")
    def test_interact(self, action_on_element_mock):
        content = [{"type": 1, "name": 2, "content": 3}, {"type": 4, "name": 5}]
        result = interact(self.driver, content)
        self.assertEqual(None, result)
        call_args = action_on_element_mock.call_args_list
        self.assertEqual((self.driver, 1, 2, 3), list(call_args[0])[0])
        self.assertEqual((self.driver, 4, 5, None), list(call_args[1])[0])
        self.driver.reset()

    def test_action_on_element_invisible_field(self):
        setup_actions.By = mocks.By()
        self.driver.elem_visible = False
        setup_actions.action_on_element(self.driver, "id", "name", "content")
        self.assertEqual("javascript:document.getElementById('name').value=content;", self.driver.last_script)
        self.driver.elem_visible = True
        self.driver.reset()

    def test_action_on_element_visible_field(self):
        setup_actions.By = mocks.By()
        setup_actions.action_on_element(self.driver, "id", "name", "content")
        self.assertTrue(self.driver.last_elem.send_keys_called)
        self.driver.reset()

    def test_action_on_element_xpath(self):
        setup_actions.By = mocks.By()
        setup_actions.action_on_element(self.driver, "xpath", "name")
        self.assertEqual(
            """document.evaluate("name", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""",
            self.driver.last_script)
        self.driver.reset()

    def test_action_on_element_tag(self):
        setup_actions.By = mocks.By()
        setup_actions.action_on_element(self.driver, "tag_name", "name")
        self.assertTrue(self.driver.last_elem.click_called)
        self.driver.reset()

    def test_action_on_element(self):
        setup_actions.By = mocks.By()
        setup_actions.action_on_element(self.driver, "id", "name")
        self.assertTrue("javascruipt:document.getElementById('name').click()", self.driver.last_script)
        self.driver.reset()

    def test_action_on_element_element_error(self):
        setup_actions.By = mocks.By()
        self.driver.throw_no_such_elem_error = True
        result = setup_actions.action_on_element(self.driver, "id", "name", "content")
        self.assertEqual(1, result)
        self.driver.reset()

    @patch("BrowserAutomator.setup_actions.actions_from_variable", side_effect=lambda actions: actions)
    @patch("BrowserAutomator.setup_actions.run_functions", side_effect=lambda driver, functions: 0)
    def test_for_every_good(self, run_functions_mock, actions_from_variable_mock):
        content = {"urls": [self.url_0, self.url_1],
                   "actions": [
                       {"load": ""}
                   ]}
        result = for_every(self.driver, content)
        self.assertEqual(None, result)
        self.assertEqual(actions_from_variable_mock.call_args_list[0][0][0], [{'load': self.url_0}])
        self.assertEqual(actions_from_variable_mock.call_args_list[1][0][0], [{'new_tab': self.url_1}])
        self.assertEqual((self.driver, [{'load': self.url_0}]), run_functions_mock.call_args_list[0][:1][0])
        self.assertEqual((self.driver, [{'new_tab': self.url_1}]), run_functions_mock.call_args_list[1][:1][0])

    @patch("BrowserAutomator.setup_actions.actions_from_variable", side_effect=lambda actions: actions)
    @patch("BrowserAutomator.setup_actions.run_functions", side_effect=lambda driver, functions: 1)
    def test_for_every_bad(self, run_functions_mock, actions_from_variable_mock):
        content = {"urls": [self.url_0, self.url_1],
                   "actions": [
                       {"load": ""}
                   ]}
        result = for_every(self.driver, content)
        self.assertEqual(1, result)
        self.assertEqual(actions_from_variable_mock.call_args_list[0][0][0], [{'load': self.url_0}])
        self.assertEqual((self.driver, [{'load': self.url_0}]), run_functions_mock.call_args_list[0][:1][0])


if __name__ == '__main__':
    main()
