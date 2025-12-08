from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, AGE_CONFIRMATION_DATE


class AgeVerificationPopup:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.DATE_INPUT = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
        self.CONFIRM_BTN = (By.XPATH, "//button[text()='Confirm']")
        self.SUCCESS_MSG = (By.XPATH, "//div[contains(text(),'You are of age')]")
        self.UNDERAGE_MSG = (By.XPATH, "//div[contains(text(),'You are underage')]")

    def enter_birthdate_and_confirm(self, birthdate: str):
        """Gibt das Geburtsdatum ein und klickt auf Bestätigen"""
        date_input = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.DATE_INPUT)
        )
        date_input.clear()
        if birthdate:
            date_input.send_keys(birthdate)

        self.driver.find_element(*self.CONFIRM_BTN).click()

    def confirm_age(self, birthdate: str = AGE_CONFIRMATION_DATE):
        """Führt die Altersbestätigung mit dem Standarddatum durch"""
        try:
            self.enter_birthdate_and_confirm(birthdate)
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.DATE_INPUT)
            )
        except:
            # Fals das popup nicht inerhalb von 5 sec erscheint, ignorieren wir es
            pass

    def is_success_message_displayed(self):
        """Prüft, ob die 'Erfolgsmeldung' sichtbar ist"""
        try:
            WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.visibility_of_element_located(self.SUCCESS_MSG)
            )
            return True
        except:
            return False

    def is_warning_message_displayed(self):
        """Prüft, ob die 'Warnmeldung' sichtbar ist"""
        try:
            WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.visibility_of_element_located(self.UNDERAGE_MSG)
            )
            return True
        except:
            return False