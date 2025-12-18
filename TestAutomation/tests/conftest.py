import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from TestAutomation.pages.login_page import LoginPage
from TestAutomation.utils.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD


@pytest.fixture
def driver():
    """Stellt den Selenium WebDriver bereit und schließt ihn nach dem Test."""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # optional: Browser unsichtbar
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    """
    Führt den Login-Prozess aus und stellt den eingeloggten WebDriver bereit.
    Diese Fixture hängt von der 'driver' Fixture ab.
    """
    login_page = LoginPage(driver)

    # Navigieren zur Login-Seite
    login_page.navigate_to_login()

    # Login durchführen
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # Wichtig: Wir geben den bereits eingeloggten driver zurück
    return driver