from selenium.webdriver import ChromeOptions, Chrome


def selenium_setup(chromedriver_path=None, fullscreen=True):
    """starts a selenium chrome browser session with disabled infobars (and optionally in fullscreen)
       returns the driver"""
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    if chromedriver_path:
        driver = Chrome(chromedriver_path, chrome_options=chrome_options)
    else:
        driver = Chrome(chrome_options=chrome_options)
    if fullscreen:
        driver.fullscreen_window()
    return driver
