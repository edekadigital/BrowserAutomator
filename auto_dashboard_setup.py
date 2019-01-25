from selenium_setup import selenium_setup
from setup_actions import action_runner
from loop_actions import loop_runner
from os import environ


def setup():
    driver = selenium_setup()
    action_runner(driver)
    loop_runner(driver)


if __name__ == "__main__":
    # environ["CHROMEDRIVER"] = './chromedriver'
    setup()
