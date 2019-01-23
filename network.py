from os import system
from time import sleep
from actions import action_runner


def check_network_not_working():
    """pings Google to determine whether internet access is available
       returns True if internet isn't available, and False if it is"""
    try:
        response = system("ping -c 1 1.1.1.1")
    except:
        return True
    return False if response == 0 else True


def fix_wifi(driver):
    """periodically checks if the internet still works, and logs back in otherwise"""
    while True:
        if check_network_not_working():
            print('Network not working')
            sleep(60)
            action_runner(driver)
        sleep(60)
