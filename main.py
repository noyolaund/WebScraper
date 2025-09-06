from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome, Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from datetime import datetime

filename = datetime.now().strftime("logs/logfile_%Y-%m-%d_%H-%M-%S.log")

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [
    logging.FileHandler(filename),
    logging.StreamHandler()
])

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1820,980')
driver = Chrome(service=service, options=options)

def close_pop_up_window():
    try:
        popup_window = driver.find_element(By.NAME, "//*[@id='header-section']/button[1]/div[1]/svg[1]/g[1]/g[1]/path[1]")
        popup_window.click()
        logging.info("Popup window closed...")
        time.sleep(2)
    except NoSuchElementException:
        logging.info("Popup window not found...")

def main():

    driver.get("https://mybees.mx")
    logging.info("Starting automation...")
    time.sleep(2)

    cookie_accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookie_accept.click()
    time.sleep(2)

    login_button = driver.find_element(By.NAME, "guest_homepage_login_button")
    login_button.click()
    logging.info("Login page...")
    time.sleep(3)

    email = driver.find_element(By.ID, "signInName")
    email.send_keys("noyolaund@gmail.com")
    password = driver.find_element(By.ID, "password")
    password.send_keys("AmdsamIP75b")
    time.sleep(2)
    password.send_keys(Keys.ENTER)
    time.sleep(5)
    logging.info("Login complete...")

    close_pop_up_window()

    offers_button = driver.find_element(By.XPATH, "//*[@id='menu']/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/h2[1]/a[1]")
    offers_button.click()
    logging.info("Offers button clicked...")
    time.sleep(2)

    close_pop_up_window()

    names = driver.find_elements(By.CSS_SELECTOR, "span.bees-text.bees-product-card-title")
    for index, name in enumerate(names):
        logging.info(f"{index}: {name.text}")

    time.sleep(5)

    driver.quit()
    logging.info("Test completed...")

if __name__ == "__main__":
    main()