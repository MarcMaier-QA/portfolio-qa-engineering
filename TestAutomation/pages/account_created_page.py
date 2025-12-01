from selenium.webdriver.common.by import By
from .base_page import BasePage


class AccountCreatedPage(BasePage):

    CREATED = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def verify_created(self):
        return self.visible(self.CREATED)

    def continue_click(self):
        self.click(self.CONTINUE)
