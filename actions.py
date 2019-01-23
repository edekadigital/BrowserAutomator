from selenium.webdriver.common.by import By
from selenium import webdriver
from json import load
from os.path import exists
from time import sleep


def action_runner(driver):
    """reads actions from json and runs them"""
    actions = read_actions()
    run_actions(driver, actions)


def run_actions(driver, actions):
    """given a list of actions, this function executes them"""
    for action in actions:
        action_mapper(driver, action['type'], action['content'])


def read_actions(filename='actions.json'):
    """given a config file, reads the contained actions
       returns them as a list of actions
       file -> [{'type':'wait', 'content': '60'},]"""
    if not exists(filename):
        return []
    with open(filename) as file:
        actions = load(file)
    return actions


def action_mapper(driver, action_type, content=None):
    types = {"wait": wait, "load": load_url, "new_tab": new_tab, "switch_tabs": switch_tabs, "interact": interact,
             "repeat": repeater}
    f = types.get(action_type, action_on_element)
    f(driver, content)


def wait(driver, content):
    """given a time to wait in seconds as `content`, blocks for the amount of seconds"""
    sleep(int(content))


def load_url(driver, content):
    """given a url as `content`, opens the url"""
    driver.get(content)


def new_tab(driver: webdriver.Chrome, content):
    """given a url as `content`, opens the url in a new tab"""
    driver.execute_script("window.open('about:blank','_blank');")
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[1])
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


def repeater(driver, content):
    urls, actions = content["urls"], content["actions"]
    for i in range(len(urls)):
        # injecting the current url
        for action in actions:
            if (action["type"] == "load" or action["type"] == "new_tab"):
                action["content"] = urls[i]
                if i > 0:
                    action["type"] = "new_tab"
        run_actions(driver, actions)


if __name__ == "__main__":
    print(read_actions())
