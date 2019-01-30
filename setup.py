from selenium_setup import selenium_setup
from setup_actions import action_runner
from loop_actions import loop_runner


def setup():
    """starts the selenium session and executes the actions"""
    driver = selenium_setup()
    action_runner(driver)
    loop_runner(driver)


if __name__ == "__main__":
    setup()
