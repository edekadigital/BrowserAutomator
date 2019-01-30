from os import system
from requests import get


def check_network_not_working1():
    """pings Google to determine whether internet access is available
       returns True if internet isn't available, and False if it is"""
    try:
        response = system("ping -c 1 1.1.1.1")
    except:
        return True
    return False if response == 0 else True


def check_network_not_working():
    """requests Google and checks for redirects to determine whether internet access is available
       returns True if internet isn't available, and False if it is"""
    response = False
    try:
        req = get("https://www.google.com")
        if len(req.history):
            response = True
    except:
        response = True
    print("network not available" if response else "network available")
    return response


if __name__=="__main__":
    print(check_network_not_working())
