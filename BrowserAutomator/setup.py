from BrowserAutomator.selenium_setup import selenium_setup
from BrowserAutomator.setup_actions import action_runner
from BrowserAutomator.loop_actions import loop_runner
from BrowserAutomator.logging_util import logging_setup
from logging import ERROR
from time import sleep


def setup(setup_filenames, loop_filename, chromedriver_path="/usr/bin/chromedriver",
          log_path="/tmp/BrowserAutomator.log",
          log_level=ERROR):
    """starts the selenium session and executes the actions
        when one of the actions fail the execution gets restarted"""
    logging_setup(log_path, log_level)
    driver = selenium_setup(chromedriver_path)
    if action_runner(driver, setup_filenames) == 1:
        driver.quit()
        return 1
    out = loop_runner(driver, loop_filename, setup_filenames)
    driver.quit()
    return out


def setup_caller(setup_filename, loop_filename, chromedriver_path, log_path, log_level):
    setup(setup_filename, loop_filename, chromedriver_path, log_path, log_level)
    sleep(30)


def run(setup_filename, loop_filename, chromedriver_path="/usr/bin/chromedriver",
        log_path="/tmp/BrowserAutomator.log", log_level=None):
    while True:
        setup_caller(setup_filename, loop_filename, chromedriver_path, log_path, log_level)
