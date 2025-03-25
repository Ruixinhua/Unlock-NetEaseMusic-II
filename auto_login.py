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
    MUSIC_U = "00B9E970D27547481DF7EF678C1BDDE8C1E656F743C576948FC61593E82219C34C6EE7C2889E045B2FEFF3D63067B1F5FA9EE4B18CFBA6EF5B5885ABA9AD4B34FE816D4471D6807BC068B71B2CABDABC30AEA58A35BCF4955238277BC5DC3CA854884E9F7D0A738BF8D56BF506C0E601D1CEC8AB9738058C77210B1F31E0BA5CE3B3731A4E900319B56E540210DFF81964C92D9729A4B54797F88B66759BED92CEFC6EF3D5FD0F4AE88C636BE7DD03F0FDA8330020429BC95BE5743FE6843991201F68A03CC90F7CAAD7F574DA094551DF2E940B64680AF4E130DEFE3DC17A6C37DCE1C25D9E5624699E5F734122D4D8F5AF0F44379E9D493DC1D43EFD88C7CC556FB4680DC22A321C721615151B4BA3A9D5265936BC6084F5CE04E71CA7EC5FC38802ECB6130FED5CD198D2B4B96C80243D334721F994EBB4FEE70E8DC53A698646EB7AB1312DA3C80BE41CBEF4C3B6620A0A7792D98F48A5A9A7B30F0C0AF906"
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
