from selenium.webdriver.common.by import By
from Hausübungen.pages import SignupLoginPage
from Hausübungen.pages import AccountInfoPage
from Hausübungen.pages import AddressPage
from Hausübungen.pages import AccountCreatedPage
from Hausübungen.pages import HomePage
from Hausübungen.pages import DeleteAccountPage
from Hausübungen.userdata.user_data import user_valid


def test_registration(driver):

    driver.get("https://automationexercise.com/")

    # Signup/Login
    signup = SignupLoginPage(driver)

    # Direkt das Popup schließen, falls vorhanden
    signup.close_popup()

    # Signup/Login-Link auf der Startseite anklicken
    signup.driver.find_element(By.CSS_SELECTOR, "a[href='/login']").click()

    # Signup-Titel prüfen
    element = signup.check_signup_title()

    signup.signup(
        user_valid["account"]["name"],
        user_valid["account"]["email"]
    )

    # Account Info
    accountInfoPage = AccountInfoPage(driver)
    accountInfoPage.check_title()
    accountInfoPage.fill_account_info(user_valid["account"])

    # Address
    addressPage = AddressPage(driver)
    addressPage.fill_address(user_valid["address"])

    # Account Created
    accountCreatedPage = AccountCreatedPage(driver)
    accountCreatedPage.verify_created()
    accountCreatedPage.continue_click()

    # Logged in
    homePage = HomePage(driver)
    homePage.check_logged_in()
    homePage.delete_account()

    # Account Deleted
    deleteAccountPage = DeleteAccountPage(driver)
    deleteAccountPage.verify_deleted()
    deleteAccountPage.continue_click()
