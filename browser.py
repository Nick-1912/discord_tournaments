from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_browser():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--kiosk')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/home/nick/chromedriver', options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver
