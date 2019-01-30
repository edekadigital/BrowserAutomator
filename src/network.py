from os import system


def check_network_not_working():
    """pings Google to determine whether internet access is available
       returns True if internet isn't available, and False if it is"""
    try:
        response = system("ping -c 1 1.1.1.1")
    except:
        return True
    return False if response == 0 else True



