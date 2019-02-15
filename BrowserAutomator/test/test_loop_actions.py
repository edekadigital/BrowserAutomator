from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator import loop_actions
from BrowserAutomator.test.mocks import LoopObjMock, SeleniumMock, PeriodicallyCheckMock, DatetimeMock

loop_actions.datetime = DatetimeMock


class LoopActionsTest(TestCase):
    filenames, setup_filename = ["filename"], "setup_filename"
    driver = SeleniumMock()
    content = [{"seconds": 2}]

    @patch("BrowserAutomator.loop_actions.get_actions",
           side_effect=lambda filename, all_actions: [(lambda x: x + "_1", "content")])
    def test_get_action_objects(self, get_actions_mock):
        all_actions = {'repeat every': loop_actions.RepeatEvery, 'fix wifi': loop_actions.WifiFixer,
                       'switch tabs': loop_actions.TabSwitcher}
        # testing list of filenames
        result = loop_actions.get_action_objects(self.filenames)
        self.assertEqual(["content_1"], result)
        get_actions_mock.assert_called_with(self.filenames[0], all_actions)
        # testing string for filename
        result = loop_actions.get_action_objects(self.filenames[0])
        self.assertEqual(["content_1"], result)
        get_actions_mock.assert_called_with(self.filenames[0], all_actions)

    @patch("BrowserAutomator.loop_actions.sleep")
    @patch("BrowserAutomator.loop_actions.get_action_objects", side_effect=lambda filename: [LoopObjMock()])
    def test_loop_runner(self, get_action_objects_mock, sleep_mock):
        result = loop_actions.loop_runner(self.driver, self.filenames, self.setup_filename)
        get_action_objects_mock.assert_called_with(self.filenames)
        self.assertEqual(self.driver, LoopObjMock().driver)
        self.assertEqual(self.setup_filename, LoopObjMock().filename)

    def test_reset(self):
        loop_actions.reset(self.driver)
        self.assertEqual([0], self.driver.window_handles)
        self.driver.reset()

    def test_check_criteria(self):
        obj, mock_obj = loop_actions.PeriodicallyCheck(self.content), PeriodicallyCheckMock()
        obj.get_current_time = mock_obj.get_current_time
        self.assertFalse(obj.check_criteria())
        self.assertTrue(obj.check_criteria())

    def test_get_current_time(self):
        obj = loop_actions.PeriodicallyCheck(self.content)
        result = [obj.get_current_time("days"), obj.get_current_time("hours"), obj.get_current_time("minutes")]
        self.assertEqual([31, 23, 59], result)

    @patch("BrowserAutomator.loop_actions.switch_tabs", side_effect=lambda driver, tab: True)
    def test_tabswitcher(self, switch_tabs_mock):
        obj = loop_actions.TabSwitcher(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        switch_tabs_mock.assert_called_with(self.driver, 1)

    @patch("BrowserAutomator.loop_actions.check_network_not_working", side_effect=lambda: True)
    @patch("BrowserAutomator.loop_actions.action_runner", side_effect=lambda driver, tab: True)
    def test_wifi_fixer(self, action_runner_mock, network_check_mock):
        obj = loop_actions.WifiFixer(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        action_runner_mock.assert_called_with(self.driver, self.setup_filename)
        network_check_mock.assert_called_once()

    @patch("BrowserAutomator.loop_actions.action_runner", side_effect=lambda driver, tab: True)
    def test_repeat_every(self, action_runner_mock):
        obj = loop_actions.RepeatEvery(self.content)
        obj.check_criteria = lambda: False
        self.assertIsNone(obj.run_task(self.driver, self.setup_filename))
        obj.check_criteria = lambda: True
        self.assertTrue(obj.run_task(self.driver, self.setup_filename))
        action_runner_mock.assert_called_with(self.driver, self.setup_filename)


if __name__ == '__main__':
    main()
