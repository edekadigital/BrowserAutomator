from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, NoSuchWindowException, \
    JavascriptException
from selenium import webdriver
from time import sleep
from logging import getLogger
from BrowserAutomator.runner import get_actions, get_action_functions
from BrowserAutomator.cipher_util import decrypt_content

logger = getLogger(__name__)


def get_all_actions():
    all_actions = {"zoom": zoom, "wait": wait, "wait for": wait_for, "load": load_url, "new_tab": new_tab,
                   "switch_tabs": switch_tabs, "interact": interact, "for every": for_every}
    return all_actions


def actions_from_file(filename):
    """reads the given file
       returns a list of tuples of all the functions specified inside the setup file with their parameters"""
    all_actions = get_all_actions()
    actions = get_actions(filename, all_actions)
    return actions


def actions_from_variable(actions):
    """given a list of actions
       returns a list of tuples of all the functions specified inside the actions list with their parameters"""
    all_actions = get_all_actions()
    actions = get_action_functions(actions, all_actions)
    return actions


def run_functions(driver, actions, wait_for_it=False):
    """given a list of function-parameter tuples, runs each function"""
    for func, content in actions:
        if func(driver, content, wait_for_it=wait_for_it) == 1:
            if not wait_for_it:
                logger.error("function {0} failed to execute with content: {1}".format(func, content))
            return 1


def action_runner(driver, filenames):
    """gets the action function-parameter tuples and runs them"""
    if type(filenames) == str:
        actions = actions_from_file(filenames)
        return run_functions(driver, actions)
    else:
        for filename in filenames:
            actions = actions_from_file(filename)
            if run_functions(driver, actions) == 1:
                return 1


def zoom(driver, content, wait_for_it=False):
    driver.execute_script("document.body.style.zoom = '{0}';".format(content))


def wait(driver, content, wait_for_it=False):
    """given a time to wait in seconds as `content`, blocks for the amount of seconds"""
    units = {"days": lambda x: 24 * 60 * 60 * x, "hours": lambda x: 60 * 60 * x, "minutes": lambda x: 60 * x,
             "seconds": lambda x: x}
    # extracting the content
    if type(content) == list:
        content = content[0]
    unit, amount = tuple(content.items())[0]
    sleep(units[unit](amount))


def wait_for(driver, content, wait_for_it=False):
    """given an action/a list of actions, tries to run it until it is successful"""
    if type(content) == list:
        actions = actions_from_variable(content)
    else:
        actions = actions_from_variable([content])
    while run_functions(driver, actions, wait_for_it=True) == 1:
        sleep(0.1)


def load_url(driver, content, wait_for_it=False):
    """given a url as `content`, opens the url"""
    driver.get(content)


def new_tab(driver: webdriver.Chrome, content, wait_for_it=False):
    """given a url as `content`, opens the url in a new tab"""
    try:
        driver.execute_script("window.open('about:blank','_blank');")
    except JavascriptException:
        if not wait_for_it:
            logger.error("Failure opening a new tab")
        return 1
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[-1])
    return load_url(driver, content)


def switch_tabs(driver: webdriver.Chrome, content, wait_for_it=False):
    """given an tab index as `content`, switches to the given tab"""
    windows = driver.window_handles
    if len(windows) > int(content):
        try:
            driver.switch_to.window(windows[content])
        except NoSuchWindowException:
            if not wait_for_it:
                logger.error("Failure switching tabs", exc_info=True)
            return 1


def interact(driver, content, wait_for_it=False):
    """given a list of actions on elements, executes the actions"""
    if type(content) is not list:
        content = [content]
    for action in content:
        interaction_content = action.get('content', None)
        result = action_on_element(driver, action['type'], action['name'], interaction_content, wait_for_it=wait_for_it)
        if result == 1:
            if not wait_for_it:
                logger.debug("interaction failed")
            return 1


def get_js_command(elem_type, name, content=None):
    js_types = {"id": "getElementById", "name": "getElementsByName", "class": "getElementsByClassName"}
    js_type = js_types[elem_type]
    js = "javascript:document.{0}('{1}')".format(js_type, name)
    if js_type[:11] == "getElements":
        js += "[0]"
    if content:
        js += ".value={0};".format(content)
    else:
        js += ".click();"
    return js


def action_on_element(driver: webdriver.Chrome, elem_type, name, content=None, wait_for_it=False):
    """given the type of an element and its name
       clicks the element from the site or writes `content` into it if it is specified"""
    types = {"id": By.ID, "name": By.NAME, "class": By.CLASS_NAME, "css": By.CSS_SELECTOR, "xpath": By.XPATH,
             "tag_name": By.TAG_NAME}
    try:
        elem = driver.find_element(types[elem_type], name)
    except (NoSuchElementException, NoSuchAttributeException):
        if not wait_for_it:
            logger.error("element not found: {0} {1}".format(elem_type, name))
        return 1
    # text field events
    if content:
        if type(content) == list or type(content) == dict:
            # cipher stuff
            content = decrypt_content(content)
        # visible text field
        if not elem.is_displayed():
            js = get_js_command(elem_type, name, content)
            driver.execute_script(js)
        # invisible text field
        else:
            elem.send_keys(content)

    # click events
    elif elem_type == "xpath":
        js = """document.evaluate("{0}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""".format(
            name)
        driver.execute_script(js)
    # button
    elif elem_type == "tag_name":
        elem.click()
    # invisible button
    else:
        js = get_js_command(elem_type, name)
        driver.execute_script(js)


def for_every(driver, content, wait_for_it=False):
    """given a list of urls and a list of actions
       executes all of the actions for each url"""
    urls, actions = content["urls"], content["actions"]
    all_actions = []
    for i in range(len(urls)):
        # injecting the current url into load/net_tab actions
        for action in actions:
            action_type, content = next(iter(action.items()))
            if action_type == "load" or action_type == "new_tab":
                if i > 0:
                    action.pop(action_type)
                    action["new_tab"] = urls[i]
                else:
                    action[action_type] = urls[i]
        all_actions.append([dict(action) for action in actions])
        functions = actions_from_variable(all_actions[-1])
        if run_functions(driver, functions, wait_for_it=wait_for_it) == 1:
            return 1
