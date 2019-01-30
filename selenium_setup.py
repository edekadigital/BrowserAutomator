from selenium import webdriver


def selenium_setup(chromedriver_path="/usr/lib/chromium-browser/chromedriver", fullscreen=True):
    """starts a selenium chrome browser session with disabled infobars (and optionally in fullscreen)
       returns the driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    if fullscreen:
        driver.fullscreen_window()
    return driver


if __name__ == "__main__":
    pass
