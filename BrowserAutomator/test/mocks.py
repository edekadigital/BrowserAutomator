from selenium.common.exceptions import JavascriptException, NoSuchWindowException


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

        def quit(self):
            self.quit_called = True

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


if __name__ == "__main__":
    x = SeleniumMock()
    y = SeleniumMock()
    print(x, y)
