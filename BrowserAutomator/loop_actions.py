from datetime import datetime
from BrowserAutomator.network import check_network_not_working
from BrowserAutomator.setup_actions import switch_tabs, action_runner
from BrowserAutomator.runner import get_actions
from time import sleep


def get_action_objects(filenames):
    """reads the actions from all yml files given in `filenames` and returns the objects specified in it"""
    all_actions = {'repeat every': RepeatEvery, 'fix wifi': WifiFixer, 'switch tabs': TabSwitcher}
    if type(filenames) == str:
        actions = get_actions(filenames, all_actions)
    else:
        actions = []
        for filename in filenames:
            actions += get_actions(filename, all_actions)
    # create all objects
    all_objs = [obj(content) for obj, content in actions]
    return all_objs


def loop_runner(driver, filenames, setup_filenames):
    """calls the run_task function of all objects"""
    all_objs = get_action_objects(filenames)
    while True:
        for action in all_objs:
            out = action.run_task(driver, setup_filenames)
            if out == 1:
                return 1
        sleep(0.5)


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
    def run_task(self, driver, setup_filenames):
        if self.check_criteria():
            open_tabs = len(driver.window_handles)
            self.current_tab = (self.current_tab + 1) % open_tabs
            return switch_tabs(driver, self.current_tab)


class WifiFixer(PeriodicallyCheck):
    """checks every_n time_units if the network is working and returns True if it doesn't"""
    def run_task(self, driver, setup_filenames):
        if self.check_criteria():
            if check_network_not_working():
                # if the network isn't working the setup gets rerun
                return action_runner(driver, setup_filenames)


class RepeatEvery(PeriodicallyCheck):
    """runs the setup every_n time_units"""
    def run_task(self, driver, setup_filenames):
        if self.check_criteria():
            print("repeating")
            reset(driver)
            return action_runner(driver, setup_filenames)
