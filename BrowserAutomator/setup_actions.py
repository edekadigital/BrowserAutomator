from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, NoSuchWindowException, \
    JavascriptException
from selenium import webdriver
from time import sleep
from BrowserAutomator.runner import get_actions, get_action_functions

def get_all_actions():
    all_actions = {"zoom": zoom, "wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs,
                   "interact": interact, "for every": for_every}
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


def run_functions(driver, actions):
    """given a list of function-parameter tuples, runs each function"""
    for func, content in actions:
        if func(driver, content) == 1:
            print("function {0} failed to execute with content: {1}".format(func, content))
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


def zoom(driver, content):
    driver.execute_script("document.body.style.zoom = '{0}';".format(content))


def wait(driver, content):
    """given a time to wait in seconds as `content`, blocks for the amount of seconds"""
    units = {"days": lambda x: 24 * 60 * 60 * x, "hours": lambda x: 60 * 60 * x, "minutes": lambda x: 60 * x,
             "seconds": lambda x: x}
    unit, amount = tuple(content[0].items())[0]
    sleep(units[unit](amount))


def load_url(driver, content):
    """given a url as `content`, opens the url"""
    driver.get(content)


def new_tab(driver: webdriver.Chrome, content):
    """given a url as `content`, opens the url in a new tab"""
    try:
        driver.execute_script("window.open('about:blank','_blank');")
    except JavascriptException:
        return 1
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[-1])
    return load_url(driver, content)


def switch_tabs(driver: webdriver.Chrome, content):
    """given an tab index as `content`, switches to the given tab"""
    windows = driver.window_handles
    if len(windows) > int(content):
        try:
            driver.switch_to.window(windows[content])
        except NoSuchWindowException:
            return 1


def interact(driver, content):
    """given a list of actions on elements, executes the actions"""
    for action in content:
        interaction_content = action.get('content', None)
        result = action_on_element(driver, action['type'], action['name'], interaction_content)
        if result == 1:
            print("interaction failed")
            return 1


def action_on_element(driver: webdriver.Chrome, elem_type, name, content=None):
    """given the type of an element and its name
       clicks the element from the site or writes `content` into it if it is specified"""
    types = {"id": By.ID, "name": By.NAME, "class": By.CLASS_NAME, "css": By.CSS_SELECTOR, "xpath": By.XPATH,
             "tag_name": By.TAG_NAME}
    js_types = {"id": "getElementById", "name": "getElementsByName[0]", "class": "getElementsByClassName[0]"}
    try:
        elem = driver.find_element(types[elem_type], name)
    except (NoSuchElementException, NoSuchAttributeException):
        print("element not found: {0} {1}".format(elem_type, name))
        return 1
    # visible text field
    if not elem.is_displayed() and content:
        js = "{0}{1}('{2}').value={3};".format("javascript:document.", js_types[elem_type], name, content)
        driver.execute_script(js)
    # invisible text field
    elif content:
        elem.send_keys(content)
    elif elem_type == "xpath":
        js = """document.evaluate("{0}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""".format(
            name)
        driver.execute_script(js)
    # button
    elif elem_type == "tag_name":
        elem.click()
    # invisible button
    else:
        js = "{0}{1}('{2}').click();".format("javascript:document.", js_types[elem_type], name)
        driver.execute_script(js)


def for_every(driver, content):
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
        if run_functions(driver, functions) == 1:
            return 1
