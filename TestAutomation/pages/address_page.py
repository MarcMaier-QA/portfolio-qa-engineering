from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from .base_page import BasePage

class AddressPage(BasePage):
    FIRST = (By.ID, "first_name")
    LAST = (By.ID, "last_name")
    COMPANY = (By.ID, "company")
    ADDRESS1 = (By.ID, "address1")
    ADDRESS2 = (By.ID, "address2")
    COUNTRY = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIP = (By.ID, "zipcode")
    MOBILE = (By.ID, "mobile_number")
    CREATE = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    def fill_address(self, addr):
        self.type(self.FIRST, addr["first_name"])
        self.type(self.LAST, addr["last_name"])
        self.type(self.COMPANY, addr["company"])
        self.type(self.ADDRESS1, addr["address"])
        self.type(self.ADDRESS2, addr["address2"])

        # Country Dropdown
        Select(self.driver.find_element(*self.COUNTRY)).select_by_visible_text(addr["country"])

        self.type(self.STATE, addr["state"])
        self.type(self.CITY, addr["city"])
        self.type(self.ZIP, addr["zipcode"])
        self.type(self.MOBILE, addr["mobile_number"])

        # CREATE-Button scrollen & klicken
        self.scroll_and_click(self.CREATE)

