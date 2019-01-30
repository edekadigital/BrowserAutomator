from src.selenium_setup import selenium_setup
from src.setup_actions import action_runner
from src.loop_actions import loop_runner


def setup():
    """starts the selenium session and executes the actions"""
    while True:
        driver = selenium_setup()
        action_runner(driver)
        loop_runner(driver)
        driver.quit()
