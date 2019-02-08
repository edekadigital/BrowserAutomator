from BrowserAutomator.selenium_setup import selenium_setup
from BrowserAutomator.setup_actions import action_runner
from BrowserAutomator.loop_actions import loop_runner
from time import sleep


def setup(setup_filenames, loop_filename, chromedriver_path="/usr/lib/chromium-browser/chromedriver"):
    """starts the selenium session and executes the actions
        when one of the actions fail the execution gets restarted"""
    driver = selenium_setup(chromedriver_path)
    if action_runner(driver, setup_filenames) == 1:
        driver.quit()
        return 1
    out = loop_runner(driver, loop_filename, setup_filenames)
    driver.quit()
    return out


def setup_caller(setup_filename, loop_filename, chromedriver_path):
    setup(setup_filename, loop_filename, chromedriver_path)
    sleep(30)


def run(setup_filename, loop_filename, chromedriver_path="/usr/lib/chromium-browser/chromedriver"):
    while True:
        setup_caller(setup_filename, loop_filename, chromedriver_path)
