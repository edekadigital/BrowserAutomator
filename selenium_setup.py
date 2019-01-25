from selenium import webdriver


def selenium_setup(fullscreen=True):
    chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    if fullscreen:
        driver.fullscreen_window()
    return driver


if __name__ == "__main__":
    pass