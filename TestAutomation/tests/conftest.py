import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from TestAutomation.pages.login_page import LoginPage
from TestAutomation.pages.product_page import ProductPage
from TestAutomation.utils.constants import (
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    PRODUCT_ORANGES_URL,
    PRODUCT_PEARS_URL,
    PRODUCT_CHERRIES_URL
)


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    return driver


@pytest.fixture
def oranges_product_page(login):
    page = ProductPage(login)
    page.open(PRODUCT_ORANGES_URL)
    yield page
    page.delete_my_review()  # Bewertung nach dem test Löschen.


@pytest.fixture
def pears_product_page(login):
    page = ProductPage(login)
    page.open(PRODUCT_PEARS_URL)
    yield page
    page.delete_my_review()  # Bewertung nach dem test Löschen.


@pytest.fixture
def cherries_product_page(login):
    page = ProductPage(login)
    page.open(PRODUCT_CHERRIES_URL)
    return page
