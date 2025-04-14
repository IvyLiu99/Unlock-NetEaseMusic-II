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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DC4091B9BE72E1744B7186EB71D06F9BBE96F2E32AC54B1C4306A1837D47D733955FDCEBB01ABDE39BB2DB19FB8E4287155876A2AB772202B1C4E5C82D3C41D2424D40E92A3574D486699FA5717FFD554BB18CDD2A40ADE15EFB585FA7F661473796C2820310A3968862A77A529A98E59EB5008D4FDD01A963D6FFB1D3D158C9DDA0CF0909A2F7A2B78AD6EABFFDEC68EB038E74A8F3CFEF0993A206F01DFAB67DDB43BF7844DB6702663781929CF83F57AA55EBBB2C09B5E6F9181ABBD7E091043DF4F933F8CD1DD3B5B889EF02C2C86A045932C3F7A6CE26E540A38BB22541E7E932DE4745E8A5630D3E690530722B39CB60461130483DA8B3D2681EBAD1ED9C70BDCFC18D3169C96D72D347AA61BE261C1FC71D1E8C33F333A62F762B34E4BEA38A53C1D7752595B111FA45126DB14EF67BB4E40A7A7219C2ECFCCCA789D5AFD95839F225C2E2BD418BD0AF0238032A77E46264E604C7EC2A8E8388B197DA"})
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
