from datetime import datetime
from network import check_network_not_working
from setup_actions import switch_tabs, action_runner
from runner import get_actions


def get_action_objects():
    filename = "loop.yml"
    all_actions = {'repeat every': RepeatEvery, 'fix wifi': WifiFixer, 'switch tabs': TabSwitcher}
    actions = get_actions(filename, all_actions)
    # create all objects
    all_objs = [obj(content) for obj, content in actions]
    return all_objs


def loop_runner(driver):
    all_objs = get_action_objects()
    while True:
        for action in all_objs:
            action.run_task(driver)


def reset(driver):
    """closes all tabs except the first"""
    handles = driver.window_handles
    for handle in handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(handles[0])


class PeriodicallyCheck:
    def __init__(self, content):
        self.time_unit, self.every_n = tuple(content[0].items())[0]
        self.last_refresh = datetime.now()
        self.current_tab = 0

    def check_criteria(self):
        current_time = self.get_current_time(self.time_unit)
        if current_time % self.every_n == 0 and current_time != self.last_refresh:
            self.last_refresh = current_time
            return True
        return False

    @staticmethod
    def get_current_time(unit):
        now = datetime.now()
        time = {"days": now.day, "hours": now.hour, "minutes": now.minute, "seconds": now.second}
        return time[unit]


class TabSwitcher(PeriodicallyCheck):
    def run_task(self, driver):
        if self.check_criteria():
            open_tabs = len(driver.window_handles)
            self.current_tab = (self.current_tab + 1) % open_tabs
            switch_tabs(driver, self.current_tab)


class WifiFixer(PeriodicallyCheck):
    def run_task(self, driver):
        if self.check_criteria():
            if check_network_not_working():
                # if the network isn't working the setup gets rerun
                action_runner(driver)


class RepeatEvery(PeriodicallyCheck):
    def run_task(self, driver):
        if self.check_criteria():
            reset(driver)
            action_runner(driver)
