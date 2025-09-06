from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import logging
import pytest
import time
import 

logger = logging.getLogger(__name__)

def close_pop_up_window(driver):
    try:
        popup_window = driver.find_element(By.NAME,
                                           "//*[@id='header-section']/button[1]/div[1]/svg[1]/g[1]/g[1]/path[1]")
        popup_window.click()
        logger.info("Popup window closed...")
        time.sleep(2)
    except NoSuchElementException:
        logger.info("Popup window not found...")


class TestOffers:

    def test_offers(self, driver):

        driver.get("https://mybees.mx")
        logger.info("Starting automation...")
        time.sleep(2)

        """ cookie_accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        cookie_accept.click()
        time.sleep(2) """
        actual_url = driver.current_url
        logger.info("Web Title: ", actual_url)

        login_button = driver.find_element(By.NAME, "guest_homepage_login_button").click()
        logger.info("Login page...")
        time.sleep(3)

        email = driver.find_element(By.ID, "signInName")
        email.send_keys("noyolaund@gmail.com")
        password = driver.find_element(By.ID, "password")
        password.send_keys("AmdsamIP75b")
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        logger.info("Login complete...")

        close_pop_up_window(driver)

        offers_button = driver.find_element(By.XPATH,
                                            "//*[@id='menu']/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/h2[1]/a[1]")
        offers_button.click()
        logger.info("Offers button clicked...")
        time.sleep(2)

        actual_url = driver.current_url
        assert actual_url == "https://mybees.mx/discounts#combos"

        names = driver.find_elements(By.CSS_SELECTOR, "span.bees-text.bees-product-card-title")
        for index, name in enumerate(names):
            logging.info(f"{index}: {name.text}")

        time.sleep(3)

        logger.info("Test completed...")