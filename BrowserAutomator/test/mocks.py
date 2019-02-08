from selenium.common.exceptions import JavascriptException, NoSuchWindowException, NoSuchElementException


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
            self.last_find_element_call, self.elem_visible = [], True
            self.last_elem: ElementMock = None
            self.window_handles = [0, 1]
            self.throw_js_error, self.throw_no_such_elem_error = False, False

        def fullscreen_window(self):
            self.fullscreen = True

        def get(self, url):
            self.url = url

        def execute_script(self, script):
            if self.throw_js_error:
                raise JavascriptException
            else:
                self.last_script = script

        def find_element(self, elem_type, name):
            if self.throw_no_such_elem_error:
                raise NoSuchElementException
            else:
                self.last_find_element_call = [elem_type, name]
                self.last_elem = ElementMock(elem_type, name, self.elem_visible)
                return self.last_elem

        def close(self):
            self.window_handles.remove(self.switch_to.current_window)
            self.switch_to.current_window = self.window_handles[-1]

        def quit(self):
            self.quit_called = True

        def reset(self):
            self.fullscreen, self.quit_called = False, False
            self.url, self.last_script, self.switch_to = None, None, SwitchTo()
            self.window_handles = [0, 1]
            self.throw_js_error, self.throw_no_such_elem_error = False, False
            self.last_find_element_call, self.elem_visible = [], True
            self.last_elem: ElementMock = None

    instance = None

    def __new__(cls, path=None, chrome_options=None):
        if not SeleniumMock.instance:
            SeleniumMock.instance = SeleniumMock.__SeleniumMock()
        SeleniumMock.instance.path, SeleniumMock.instance.chrome_options = path, chrome_options
        return SeleniumMock.instance


class ElementMock:
    def __init__(self, elem_type, name, visibility):
        self.type, self.name, self.visibility = elem_type, name, visibility
        self.is_displayed_called, self.send_keys_called = False, False
        self.click_called = False

    def is_displayed(self):
        self.is_displayed_called = True
        return self.visibility

    def click(self):
        self.click_called = True

    def send_keys(self, content):
        self.send_keys_called = True


class By:
    ID, NAME, CLASS_NAME, CSS_SELECTOR, XPATH, TAG_NAME = 0, 1, 2, 3, 4, 5


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


class DateTimeMock():
    def __init__(self, year, month, day, hour, minute, second, ms):
        self.year, self.month, self.day, self.hour, self.minute, self.second, self.ms = year, month, day, hour, minute, second, ms

    @classmethod
    def now(cls):
        return cls(2019, 12, 31, 23, 59, 59, 999999)


DatetimeMock = DateTimeMock(2019, 12, 31, 23, 59, 59, 999999)

if __name__ == "__main__":
    x = SeleniumMock()
    y = SeleniumMock()
    print(x, y)
