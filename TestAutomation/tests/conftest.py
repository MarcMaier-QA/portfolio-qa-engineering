import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from TestAutomation.pages.checkout_page import CheckoutPage
from TestAutomation.pages.home_page import HomePage
from TestAutomation.pages.login_page import LoginPage
from TestAutomation.pages.product_page import ProductPage
from TestAutomation.utils.constants import (
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    AGE_CONFIRMATION_DATE
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
def adult_shop(login):
    driver = login
    home_page = HomePage(driver)
    shop_page = home_page.go_to_shop()
    checkout_page = CheckoutPage(driver)

    popup = shop_page.age_popup
    if popup.is_popup_displayed():
        popup.submit_birthdate(AGE_CONFIRMATION_DATE)

    shop_page.wait_until_shop_ready()
    yield shop_page

    checkout_page.clear_cart_if_not_empty()


@pytest.fixture
def clean_cart(login):
    driver = login
    checkout_page = CheckoutPage(driver)

    yield driver

    checkout_page.clear_cart_if_not_empty()


@pytest.fixture
def shop(login):
    driver = login

    checkout_page = CheckoutPage(driver)
    checkout_page.clear_cart_if_not_empty()

    home_page = HomePage(login)
    shop_page = home_page.go_to_shop()

    yield shop_page

    checkout_page.clear_cart_if_not_empty()


@pytest.fixture
def cleanup_review(driver):
    """
    Löscht nach dem Test eine evtl. abgegebene Bewertung,
    damit Rating-Tests wiederholbar bleiben.
    """
    yield

    product_page = ProductPage(driver)
    product_page.delete_my_review()
