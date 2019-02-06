from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.loop_actions import *
from BrowserAutomator.test.mocks import LoopObjMock, SeleniumMock, PeriodicallyCheckMock, DatetimeMock

datetime = DatetimeMock


class LoopActionsTest(TestCase):
    filename, setup_filename = "filename", "setup_filename"
    driver = SeleniumMock()
    content = [{"seconds": 2}]

    @patch("BrowserAutomator.loop_actions.get_actions", side_effect=lambda filename, all_actions: [(lambda x: x + "_1", "content")])
    def test_get_action_objects(self, get_actions_mock):
        result = get_action_objects(self.filename)
        self.assertEqual(["content_1"], result)
        get_actions_mock.assert_called_with(self.filename, {'repeat every': RepeatEvery, 'fix wifi': WifiFixer, 'switch tabs': TabSwitcher})

    @patch("BrowserAutomator.loop_actions.sleep")
    @patch("BrowserAutomator.loop_actions.get_action_objects", side_effect=lambda filename: [LoopObjMock()])
    def test_loop_runner(self, get_action_objects_mock, sleep_mock):
        result = loop_runner(self.driver, self.filename, self.setup_filename)
        get_action_objects_mock.assert_called_with(self.filename)
        self.assertEqual(self.driver, LoopObjMock().driver)
        self.assertEqual(self.setup_filename, LoopObjMock().filename)

    def test_reset(self):
        reset(self.driver)
        self.assertEqual([0], self.driver.window_handles)
        self.driver.reset()

    def test_check_criteria(self):
        obj, mock_obj = PeriodicallyCheck(self.content), PeriodicallyCheckMock()
        obj.get_current_time = mock_obj.get_current_time
        self.assertFalse(obj.check_criteria())
        self.assertTrue(obj.check_criteria())

    @patch("BrowserAutomator.loop_actions.datetime", side_effect=DatetimeMock)
    def test_get_current_time(self, datetime_mock):
        """ TODO
        obj = PeriodicallyCheck(self.content)
        print(obj.get_current_time("hours"))"""
        pass

    @patch("BrowserAutomator.loop_actions.switch_tabs", side_effect=lambda driver, tab: True)
    def test_tabswitcher(self, switch_tabs_mock):
        obj = TabSwitcher(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        switch_tabs_mock.assert_called_with(self.driver, 1)

    @patch("BrowserAutomator.loop_actions.check_network_not_working", side_effect=lambda: True)
    @patch("BrowserAutomator.loop_actions.action_runner", side_effect=lambda driver, tab: True)
    def test_wifi_fixer(self, action_runner_mock, network_check_mock):
        obj = WifiFixer(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        action_runner_mock.assert_called_with(self.driver, self.setup_filename)
        network_check_mock.assert_called_once()

    @patch("BrowserAutomator.loop_actions.action_runner", side_effect=lambda driver, tab: True)
    def test_repeat_every(self, action_runner_mock):
        obj = RepeatEvery(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        action_runner_mock.assert_called_with(self.driver, self.setup_filename)


if __name__ == '__main__':
    main()
