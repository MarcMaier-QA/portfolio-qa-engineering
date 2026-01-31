from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from TestAutomation.pages.base_page import BasePage
from TestAutomation.pages.shop_page import ShopPage


class HomePage(BasePage):

    SHOP_BUTTON = (By.XPATH, "//a[@href='/store' and text()='Shop']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait.until(EC.visibility_of_element_located(self.SHOP_BUTTON))

    def go_to_shop(self):
        self.click(self.SHOP_BUTTON)
        return ShopPage(self.driver)
