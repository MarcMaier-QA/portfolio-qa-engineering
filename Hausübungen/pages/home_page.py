from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):

    LOGGED_IN = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    DELETE = (By.XPATH, "//a[@href='/delete_account']")

    def check_logged_in(self):
        return self.visible(self.LOGGED_IN)

    def delete_account(self):
        self.click(self.DELETE)
