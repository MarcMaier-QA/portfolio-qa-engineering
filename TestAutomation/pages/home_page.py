from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from TestAutomation.pages.base_page import BasePage
from TestAutomation.pages.shop_page import ShopPage


class HomePage(BasePage):

    # Main navigation button leading to the shop page
    SHOP_BUTTON = (By.XPATH, "//a[@href='/store' and text()='Shop']")

    def __init__(self, driver):
        """
        Initializes the HomePage and waits until the page is considered loaded.

        The page is treated as ready once the Shop button is visible,
        as it represents the primary navigation entry point.
        """
        super().__init__(driver)
        self.wait.until(EC.visibility_of_element_located(self.SHOP_BUTTON))

    def go_to_shop(self):
        """
        Navigates from the home page to the shop page.

        Returns:
            ShopPage: A new instance of the ShopPage after navigation.
        """
        self.click(self.SHOP_BUTTON)
        return ShopPage(self.driver)
