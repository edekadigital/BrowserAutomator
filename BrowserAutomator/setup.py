from BrowserAutomator.selenium_setup import selenium_setup
from BrowserAutomator.setup_actions import action_runner
from BrowserAutomator.loop_actions import loop_runner
from time import sleep


def setup(setup_filename, loop_filename):
    """starts the selenium session and executes the actions
        when one of the actions fail the execution gets restarted"""
    driver = selenium_setup()
    if action_runner(driver, filename=setup_filename) == 1:
        driver.quit()
        return 1
    out = loop_runner(driver, filename=loop_filename)
    driver.quit()
    return out


def run(setup_filename, loop_filename):
    while True:
        setup(setup_filename=setup_filename, loop_filename=loop_filename)
        sleep(30)
