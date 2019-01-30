from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from src.runner import get_actions, get_action_functions


def actions_from_file():
    """reads the setup.yml file
       returns a list of tuples of all the functions specified inside the setup file with their parameters"""
    filename = "setup.yml"
    all_actions = {"wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs, "interact": interact,
                   "for every": for_every}
    actions = get_actions(filename, all_actions)
    return actions


def actions_from_variable(actions):
    """given a list of actions
       returns a list of tuples of all the functions specified inside the actions list with their parameters"""
    all_actions = {"wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs, "interact": interact,
                   "for every": for_every}
    actions = get_action_functions(actions, all_actions)
    return actions


def action_runner(driver):
    """gets the action function-parameter tuples and runs them"""
    actions = actions_from_file()
    run_functions(driver, actions)


def run_functions(driver, actions):
    """given a list of function-parameter tuples, runs each function"""
    for func, content in actions:
        func(driver, content)


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
    driver.execute_script("window.open('about:blank','_blank');")
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[-1])
    load_url(driver, content)


def switch_tabs(driver: webdriver.Chrome, content):
    """given an tab index as `content`, switches to the given tab"""
    windows = driver.window_handles
    if len(windows) > int(content):
        driver.switch_to.window(windows[content])


def interact(driver, content):
    """given a list of actions on elements, executes the actions"""
    for action in content:
        interaction_content = action.get('content', None)
        action_on_element(driver, action['type'], action['name'], interaction_content)


def action_on_element(driver: webdriver.Chrome, elem_type, name, content=None):
    """given the type of an element and its name
       clicks the element from the site or writes `content` into it if it is specified"""
    types = {"id": By.ID, "name": By.NAME, "class": By.CLASS_NAME, "css": By.CSS_SELECTOR, "xpath": By.XPATH,
             "tag_name": By.TAG_NAME}
    js_types = {"id": "getElementById", "name": "getElementsByName[0]", "class": "getElementsByClassName[0]"}

    elem = driver.find_element(types[elem_type], name)
    if not elem.is_displayed() and content:
        js = "{0}{1}('{2}').value={3};".format("javascript:document.", js_types[elem_type], name, content)
        driver.execute_script(js)
    elif content:
        elem.send_keys(content)
    elif elem_type == "xpath":
        js = """document.evaluate("{0}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();""".format(
            name)
        driver.execute_script(js)
    elif elem_type == "tag_name":
        elem.click()
    else:
        js = "{0}{1}('{2}').click();".format("javascript:document.", js_types[elem_type], name)
        driver.execute_script(js)


def for_every(driver, content):
    """given a list of urls and a list of actions
       executes all of the actions for each url"""
    urls, actions = content["urls"], content["actions"]
    for i in range(len(urls)):
        # injecting the current url into load/net_tab actions
        for action in actions:
            for action_type, content in action.items():
                if action_type == "load" or action_type == "new_tab":
                    if i > 0:
                        action.pop(action_type)
                        action["new_tab"] = urls[i]
                    else:
                        action[action_type] = urls[i]
        functions = actions_from_variable(actions)
        run_functions(driver, functions)


if __name__ == "__main__":
    pass
