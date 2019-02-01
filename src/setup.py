from src.selenium_setup import selenium_setup
from src.setup_actions import action_runner
from src.loop_actions import loop_runner
from time import sleep


def setup():
    """starts the selenium session and executes the actions
        when one of the actions fail the execution gets restarted"""
    while True:
        driver = selenium_setup()
        if action_runner(driver) == 1 or loop_runner(driver) == 1:
            driver.quit()
            sleep(30)
            continue
