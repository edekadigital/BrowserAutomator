from datetime import datetime
from src.network import check_network_not_working
from src.setup_actions import switch_tabs, action_runner
from src.runner import get_actions


def get_action_objects():
    """reads the actions from loop.yml and returns the objects specified in it"""
    filename = "loop.yml"
    all_actions = {'repeat every': RepeatEvery, 'fix wifi': WifiFixer, 'switch tabs': TabSwitcher}
    actions = get_actions(filename, all_actions)
    # create all objects
    all_objs = [obj(content) for obj, content in actions]
    return all_objs


def loop_runner(driver):
    """calls the run_task function of all objects"""
    all_objs = get_action_objects()
    while True:
        for action in all_objs:
            out = action.run_task(driver)
            if out:
                return


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
        """returns True if the current_time is a multiple of every_n
           Example: every_n = 15, time_unit = seconds: returns True if 15s fits into current_time (0s, 15s, 30s, 45s)"""
        current_time = self.get_current_time(self.time_unit)
        if current_time % self.every_n == 0 and current_time != self.last_refresh:
            self.last_refresh = current_time
            return True
        return False

    @staticmethod
    def get_current_time(unit):
        """given a time unit, returns the current time in the specified unit"""
        now = datetime.now()
        time = {"days": now.day, "hours": now.hour, "minutes": now.minute, "seconds": now.second}
        return time[unit]


class TabSwitcher(PeriodicallyCheck):
    """switches to the next tab every_n time_units"""
    def run_task(self, driver):
        if self.check_criteria():
            open_tabs = len(driver.window_handles)
            self.current_tab = (self.current_tab + 1) % open_tabs
            switch_tabs(driver, self.current_tab)


class WifiFixer(PeriodicallyCheck):
    """checks every_n time_units if the network is working and returns True if it doesn't"""
    def run_task(self, driver):
        if self.check_criteria():
            if check_network_not_working():
                # if the network isn't working the setup gets rerun
                return True


class RepeatEvery(PeriodicallyCheck):
    """runs the setup every_n time_units"""
    def run_task(self, driver):
        if self.check_criteria():
            reset(driver)
            action_runner(driver)
