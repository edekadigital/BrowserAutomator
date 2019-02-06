from selenium.common.exceptions import JavascriptException, NoSuchWindowException
from datetime import datetime


class SwitchTo:
    def __init__(self):
        self.current_window = 0
        self.throw_window_error = False

    def window(self, window_handle):
        if self.throw_window_error:
            raise NoSuchWindowException
        else:
            self.current_window = window_handle


class SeleniumMock:
    """A singleton Selenium webdriver mock"""
    class __SeleniumMock:
        def __init__(self, path=None, chrome_options=None):
            self.fullscreen, self.quit_called = False, False
            self.path, self.chrome_options = path, chrome_options
            self.url, self.last_script, self.switch_to = None, None, SwitchTo()
            self.window_handles = [0, 1]
            self.throw_js_error = False

        def fullscreen_window(self):
            self.fullscreen = True

        def get(self, url):
            self.url = url

        def execute_script(self, script):
            if self.throw_js_error:
                raise JavascriptException
            else:
                self.last_script = script

        def close(self):
            self.window_handles.remove(self.switch_to.current_window)
            self.switch_to.current_window = self.window_handles[-1]

        def quit(self):
            self.quit_called = True

        def reset(self):
            self.fullscreen, self.quit_called = False, False
            self.url, self.last_script, self.switch_to = None, None, SwitchTo()
            self.window_handles = [0, 1]


    instance = None

    def __new__(cls, path=None, chrome_options=None):
        if not SeleniumMock.instance:
            SeleniumMock.instance = SeleniumMock.__SeleniumMock()
        SeleniumMock.instance.path, SeleniumMock.instance.chrome_options = path, chrome_options
        return SeleniumMock.instance


class ChromeOptions:
    def __init__(self):
        self.arguments = []

    def add_argument(self, argument):
        self.arguments.append(argument)


class RequestMock:
    def __init__(self, test_redirect=False, raise_error=False):
        if test_redirect:
            self.history = [0, 1]
        else:
            self.history = []
        if raise_error:
            raise ConnectionError


class YamlMock:
    def __init__(self, typ=None):
        self.typ = typ

    def load(self, path):
        return path


class LoopObjMock:
    class __LoopObjMock:
        def __init__(self):
            self.driver, self.filename = None, None
            self.run_task_executed = 0

        def run_task(self, driver, filename):
            """on the second run it returns 1"""
            self.driver, self.filename = driver, filename
            if self.run_task_executed >= 1:
                return 1
            self.run_task_executed += 1

    instance = None

    def __new__(cls):
        if not LoopObjMock.instance:
            LoopObjMock.instance = LoopObjMock.__LoopObjMock()
        return LoopObjMock.instance


class PeriodicallyCheckMock:
    def __init__(self):
        self.get_current_time_called = 0

    def check_criteria(self):
        pass

    def get_current_time(self, unit):
        self.get_current_time_called += 1
        return self.get_current_time_called


class DateTimeMock(datetime):
    @classmethod
    def now(cls):
        return cls(2018, 12, 31, 23, 59, 59, 999999)


DatetimeMock = DateTimeMock(2018, 12, 31, 23, 59, 59, 999999)




if __name__ == "__main__":
    x = SeleniumMock()
    y = SeleniumMock()
    print(x, y)
