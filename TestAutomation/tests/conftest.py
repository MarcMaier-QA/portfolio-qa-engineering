import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from TestAutomation.pages.login_page import LoginPage
from TestAutomation.utils.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD
from TestAutomation.pages.product_page import ProductPage


@pytest.fixture
def clean_reviews(request, login):
    """
    Gibt eine ProductPage zurück, die am Testende jede Bewertung löscht.
    """
    driver = login
    product_page = ProductPage(driver)


    # request.node = Das python-Testobjekt, das gerade ausgeführt wird
    # .get_closest_marker("product") = sucht nach @pytest.mark.product(...) am Test
    # args[0] = nimmt das erste Argument des Markers → die URL
    product_url = request.node.get_closest_marker("product").args[0]

    # zu beginn des testes navigate_to(...)
    product_page.navigate_to(product_url)

    yield product_page

    # nach dem test navigate_to() und delete
    product_page.navigate_to(product_url)
    product_page.delete_my_review()



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