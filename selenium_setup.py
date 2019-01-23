from selenium import webdriver

chromedriver_path = './chromedriver'


def selenium_setup(fullscreen=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    if fullscreen:
        driver.fullscreen_window()
    return driver
