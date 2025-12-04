from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class AccountInfoPage(BasePage):

    TITLE = (By.XPATH, "//h2/b[text()='Enter Account Information']")
    PASSWORD = (By.ID, "password")
    DAYS = (By.ID, "days")
    MONTHS = (By.ID, "months")
    YEARS = (By.ID, "years")
    NEWSLETTER = (By.ID, "newsletter")
    OFFERS = (By.ID, "optin")
    TITLE_RADIO = (By.ID, "id_gender1")

    def check_title(self):
        return self.visible(self.TITLE)

    def fill_account_info(self, data):
        # Titel
        self.scroll_and_click(self.TITLE_RADIO)

        # Passwort
        self.type(self.PASSWORD, data["password"])

        # Dropdowns
        Select(self.driver.find_element(*self.DAYS)).select_by_value(data["birth_day"])
        Select(self.driver.find_element(*self.MONTHS)).select_by_value(data["birth_month"])
        Select(self.driver.find_element(*self.YEARS)).select_by_value(data["birth_year"])

        # Checkboxen
        self.scroll_and_click(self.NEWSLETTER)
        self.scroll_and_click(self.OFFERS)

