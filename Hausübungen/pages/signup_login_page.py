from selenium.webdriver.common.by import By
from Hausübungen.pages.base_page import BasePage
from Hausübungen.helpers.waiters import Waiter

class SignupLoginPage(BasePage):
    # Locators
    POPUP_CLOSE = (By.CSS_SELECTOR, ".fc-button-label")
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    TITLE = (By.XPATH, "//h2[contains(text(),'New User Signup!')]")
    NAME_INPUT = (By.NAME, "name")
    SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.XPATH, "//button[text()='Signup']")

    def __init__(self, driver):
        super().__init__(driver)
        self.waiter = Waiter(driver)

    def close_popup(self):
        """Schließt das Cookie-Popup, falls vorhanden"""
        elements = self.driver.find_elements(*self.POPUP_CLOSE)
        if elements:
            self.waiter.clickable(self.POPUP_CLOSE).click()

    def click_signup_login_link(self):
        """Klickt auf den Signup/Login-Link auf der Startseite"""
        self.waiter.clickable(self.SIGNUP_LOGIN_LINK).click()

    def check_signup_title(self):
        """Prüft, ob der Signup-Titel sichtbar ist"""
        self.close_popup()
        return self.waiter.visible(self.TITLE)

    def signup(self, name, email):
        """Füllt Name und Email für die Account-Erstellung aus und klickt Signup"""
        self.waiter.visible(self.NAME_INPUT).send_keys(name)
        self.waiter.visible(self.SIGNUP_EMAIL_INPUT).send_keys(email)
        self.waiter.clickable(self.SIGNUP_BUTTON).click()
