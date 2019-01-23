from selenium_setup import selenium_setup
from datetime import datetime
from time import sleep
from actions import switch_tabs, action_runner


def setup():
    driver = selenium_setup()
    action_runner(driver)
    last_refresh = datetime.now().hour
    tab_switch = True
    while True:
        # check every minute if the time is a multiple of 6 and that the dashboard hasn't refreshed yet
        current_hour = datetime.now().hour
        if current_hour % 6 == 0 and current_hour != last_refresh:
            last_refresh = datetime.now().hour
            action_runner(driver)
        tab_switch = not tab_switch
        switch_tabs(driver, int(tab_switch))

        sleep(15)


if __name__ == "__main__":
    setup()