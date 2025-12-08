from selenium.webdriver.common.by import By

# Pages
from Hausübungen.pages.signup_login_page import SignupLoginPage
from Hausübungen.pages.account_info_page import AccountInfoPage
from Hausübungen.pages.address_page import AddressPage
from Hausübungen.pages.account_created_page import AccountCreatedPage
from Hausübungen.pages.home_page import HomePage
from Hausübungen.pages.delete_account_page import DeleteAccountPage

# Testdaten
from Hausübungen.userdata.user_data import user_valid


def test_registration(driver):

    driver.get("https://automationexercise.com/")

    # Signup/Login
    signup = SignupLoginPage(driver)

    # Popup schließen
    signup.close_popup()

    # Signup/Login-Link anklicken
    signup.driver.find_element(By.CSS_SELECTOR, "a[href='/login']").click()

    # Titel prüfen
    signup.check_signup_title()

    # Signup ausfüllen
    signup.signup(
        user_valid["account"]["name"],
        user_valid["account"]["email"]
    )

    # Account Info
    account_info = AccountInfoPage(driver)
    account_info.check_title()
    account_info.fill_account_info(user_valid["account"])

    # Address
    addressPage = AddressPage(driver)
    addressPage.fill_address(user_valid["address"])

    # Account Created
    accountCreatedPage = AccountCreatedPage(driver)
    accountCreatedPage.verify_created()
    accountCreatedPage.continue_click()

    # Home / Logged in
    homePage = HomePage(driver)
    homePage.check_logged_in()
    homePage.delete_account()

    # Account Deleted
    deletedAccountPage = DeleteAccountPage(driver)
    deletedAccountPage.verify_deleted()
    deletedAccountPage.continue_click()
