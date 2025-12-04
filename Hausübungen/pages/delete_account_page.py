from selenium.webdriver.common.by import By
from .base_page import BasePage


class DeleteAccountPage(BasePage):

    DELETED = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")
    CONTINUE = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def verify_deleted(self):
        return self.visible(self.DELETED), "Account deletion message not visible"

    def continue_click(self):
        self.click(self.CONTINUE)
