from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage


class AgeVerificationPopup(BasePage):


    # Locators
    POPUP_CONTAINER = (By.XPATH, "//div[contains(@class,'age-verification')]")

    DATE_INPUT = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")

    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(),'You are of age')]")
    WARNING_MESSAGE = (By.XPATH, "//div[contains(text(),'You are underage')]")


    # State checks
    def is_popup_displayed(self) -> bool:
        return self.is_visible(self.DATE_INPUT)

    def is_success_message_displayed(self) -> bool:
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_warning_message_displayed(self) -> bool:
        return self.is_visible(self.WARNING_MESSAGE)


    # Actions
    def enter_birthdate(self, birthdate: str):
        self.type(self.DATE_INPUT, birthdate)

    def confirm(self):
        self.click(self.CONFIRM_BUTTON)

    def submit_birthdate(self, birthdate: str):
        self.enter_birthdate(birthdate)
        self.confirm()
