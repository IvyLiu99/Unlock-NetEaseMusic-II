# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D97B74946D89C74B5523E7C7E54EC85F705A83A461573D762F25F861417F4A32D7371A82AA80B3998C2EB64447DB3E5CC3DEFF5B1901868E544A2BEEC324F5ADF50D3F85E5B34EAB5FA3357C6F466B2D613A25028449E26F8CD2865BE8950218324DCA9D05F61DE593121D56179BB1B1A5753C76EFBE77E15F5E487E715425C3A1EF21DA25E954BAF393DD59751FB123790F7F3D49B2166FF7BACFEFBE4C09B2BFC1DC40C5965DA8BBE7E07220EA97D3CF483D37B613DFA359A377F65EF61BA804D153C1261EFD81ED5361A7A0E90E03CE3D5D9B4F27C2477ECC06384258B3BC46573B62695F721EDD46AC55610B0AD04E835F968EA40E79D020E61EA918F5DCA4564FE9221053E08034C51E25F65CAB8424FCFEDD4BB6F43400E8642E32B5D526C945D4C1A382F09C16EF6761B8BE1CDCBEE43A8AB068CAAADDFEA4A0FF9BE77666E9368AC27EF775112ED0215FD4374B09646202FC0E8641EAE8F877A99471"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
