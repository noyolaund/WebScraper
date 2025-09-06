# General imports
import pytest
from selenium import webdriver

# Modern Selenium 4.6+ approach: Selenium Manager handles drivers automatically
import os

# Import options for headless mode
from selenium.webdriver.chrome.options import Options as ChromeOptions

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Send 'chrome' or 'firefox' as parameter for execution"
    )


@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser")
    # Default driver value
    driver = ""

    # Setup
    # print("Setting logging config...")
    # logging_config()
    print(f"\nSetting up: {browser} driver")
    if browser == "chrome":
        # Chrome options setup for headless mode
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1820,980')

        # ✅ Enable BiDi for accessibility locators
        chrome_options.set_capability("webSocketUrl", True)

        # Modern approach: Use Selenium Manager (no webdriver-manager needed)
        driver = webdriver.Chrome(options=chrome_options)

    # Implicit wait setup for our framework
    driver.implicitly_wait(5)
    yield driver
    # Tear down
    print(f"\nTear down: {browser} driver")
    driver.quit()