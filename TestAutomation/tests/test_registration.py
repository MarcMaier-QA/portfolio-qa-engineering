from selenium.webdriver.common.by import By
from ..pages.signup_login_page import SignupLoginPage
from ..pages.account_info_page import AccountInfoPage
from ..pages.address_page import AddressPage
from ..pages.account_created_page import AccountCreatedPage
from ..pages.home_page import HomePage
from ..pages.delete_account_page import DeleteAccountPage
from ..userdata.user_data import user_valid


def test_registration(driver):

    driver.get("https://automationexercise.com/")

    # Signup/Login
    signup = SignupLoginPage(driver)

    # Direkt das Popup schließen, falls vorhanden
    signup.close_popup()

    # Signup/Login-Link auf der Startseite anklicken
    signup.driver.find_element(By.CSS_SELECTOR, "a[href='/login']").click()

    # Signup-Titel prüfen
    signup.check_signup_title()

    signup.signup(
        user_valid["account"]["name"],
        user_valid["account"]["email"]
    )

    # Account Info
    acc = AccountInfoPage(driver)
    acc.check_title()
    acc.fill_account_info(user_valid["account"])

    # Address
    addr = AddressPage(driver)
    addr.fill_address(user_valid["address"])

    # Account Created
    created = AccountCreatedPage(driver)
    created.verify_created()
    created.continue_click()

    # Logged in
    home = HomePage(driver)
    home.check_logged_in()
    home.delete_account()

    # Account Deleted
    deleted = DeleteAccountPage(driver)
    deleted.verify_deleted()
    deleted.continue_click()
