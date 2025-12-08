import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """Stellt den Selenium WebDriver bereit und schließt ihn nach dem Test."""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # optional: Browser unsichtbar
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()
