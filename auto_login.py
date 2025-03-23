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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FD37B9CBFAD16980A0B50E2E8BEC04DFDC509F1CCF7A7B8ACAC732C3DDC000654C32A3987B0EE4CBBC85348D787856A337A6788C61E47D9633EB7762656B29041F0EAF94052538D19142127EC2A048499E4A35234C8591635B2A29FD1ED2C76ECDEE616CD51840B673DE7961C28C059A3028B40BA5074117834C640610439D04C2FD6DF2AF5D1840FABE24CF360727375CB449CDF931ACA9D91A4C3EC31A98907410055EA7C7EF9E96A9BFF8888BABAF61F98AEFC99C9C9904635732070AB1257D970066F2B289A52B59D1C1628E6E3DB7FCA2F670BAD5D41EF74814EDCCD201FDE6373EC63ACA3CB7B951A833E4C16391F80EE1DD0A5175496024E1510473CF07DB750F595FE7B71B2543547C5646FAB102628749AE14B8EAFD7DA186618F626253C7BA63BA183299E23F0B3E129947D26615B4640A486BC08C3A6C6260A6E7852102F9606DA3B061632A10602B198157CBB01260EABF50EDCE65E5CE96A7E4"})
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
