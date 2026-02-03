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


# Browser / Driver
@pytest.fixture
def driver():
    """
    Provides a Chrome WebDriver instance for tests.

    The browser is started maximized to avoid
    viewport-related UI issues.
    """
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver

    # Ensure browser is always closed, even if a test fails
    driver.quit()


# Authentication
@pytest.fixture
def login(driver):
    """
    Logs in with a valid test user and returns the driver.

    This fixture is intentionally kept lightweight so it
    can be reused by multiple higher-level fixtures.
    """
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    return driver


# Shop with age verification
@pytest.fixture
def adult_shop(login):
    """
    Provides a shop page with completed age verification.

    Ensures:
    - user is logged in
    - age verification popup is handled if present
    - shop is fully loaded and usable

    Automatically cleans up the cart after the test.
    """
    driver = login

    home_page = HomePage(driver)
    shop_page = home_page.go_to_shop()
    checkout_page = CheckoutPage(driver)

    popup = shop_page.age_popup
    if popup.is_popup_displayed():
        popup.submit_birthdate(AGE_CONFIRMATION_DATE)

    shop_page.wait_until_shop_ready()

    yield shop_page

    # Cleanup to keep tests independent
    checkout_page.clear_cart_if_not_empty()


# Clean cart (driver-based)
@pytest.fixture
def clean_cart(login):
    """
    Ensures the cart is empty after the test.

    Useful for tests that manage navigation themselves
    but still require a clean cart state.
    """
    driver = login
    checkout_page = CheckoutPage(driver)

    yield driver

    checkout_page.clear_cart_if_not_empty()



# Shop without age verification logic
@pytest.fixture
def shop(login):
    """
    Provides direct access to the shop page.

    The cart is cleared before and after the test to
    ensure isolation between test cases.
    """
    driver = login
    checkout_page = CheckoutPage(driver)

    checkout_page.clear_cart_if_not_empty()

    home_page = HomePage(driver)
    shop_page = home_page.go_to_shop()

    yield shop_page

    checkout_page.clear_cart_if_not_empty()


# Review cleanup
@pytest.fixture
def cleanup_review(driver):
    """
    Deletes a user review after a test run.

    This keeps rating-related tests repeatable and
    prevents state leakage between test cases.
    """
    yield

    product_page = ProductPage(driver)
    product_page.delete_my_review()
