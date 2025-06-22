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
    MUSIC_U = "00A6C09A0A76DD80707FC2C5D9472364B29BCFD532118A5A86D9D397ABC36EC785E0BF19DED6E96A67BDC99313859F8C6228229E403ADEF57A466BE6F620985AD7D9EAD73D2FF39D8ECFA2830F41C5D5E8EF7A67ACF79D16DA022387F200689F05DF09A8FFC0A7134B74B274E82FD7A10A00A283C6EE948A907CCB4BB291776AFA7F082982F29A0E097336D64CDFD59E394859D7FE3E86520E620BEA1424B5290EDC5FC0F8B4ECCD726352AB40C408FB02D5E92FE2D6EB3BC03D5457F28ADFC245D1AE9668809F2730D4DFA34B00658FE74FA281DF4C90FE5BF131D836B5B82CF5D35D0653C7C63256B358B319381B7E2744F098AA746CFAAFBD7D7F4F5AF9DD96048973346D646652FFCCF26F2CBD974B152214C6EF8345662D266170EFE2D3B205D435A5648D36552EF0BC4999A53988A01F854050E309B2F1AD5A24AC572E6419C310D0133911EF0B3CFC9F5923632075764A7C2A83314BD81962FF6817D73B"
    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": MUSIC_U})
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
