from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage
from TestAutomation.utils.constants import SHOP_URL


class ShopPage(BasePage):
    # Navigation / Filters
    SHOP_BUTTON = (By.XPATH, "//a[text()='Shop']")
    ALCOHOL_FILTER = (By.XPATH, "//a[normalize-space()='Alocohol']")
    UNDERAGE_NOTICE = (By.XPATH, "//h2[normalize-space()='Underage Notice']")

    # Products
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class,'product-card')]")

    def PRODUCT_CARD_BY_NAME(self, name: str):
        return (
            By.XPATH,
            f"//p[@class='lead' and normalize-space()='{name}']"
            f"/ancestor::div[contains(@class,'product-card')]"
        )

    # Product actions
    QUANTITY_INPUT = (By.XPATH, ".//input[@type='number']")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@class,'btn-cart')]")

    # Pagination
    NEXT_PAGE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'pagination-link') and normalize-space()='Next']"
    )


    # Navigation
    def open_shop(self):
        """Open shop via URL"""
        self.open(SHOP_URL)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))

    def click_shop_button(self):
        """Navigate to shop via header button"""
        self.click(self.SHOP_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))

    def filter_alcohol(self):
        """Click the alcohol filter"""
        self.click(self.ALCOHOL_FILTER)
        self.wait.until(EC.presence_of_element_located(self.UNDERAGE_NOTICE))


    # Product search
    def find_product_card(self, product_name: str, max_pages: int = 10) -> WebElement | None:
        """
        Searches for a product across paginated shop pages.
        Returns the product card WebElement or None if not found.
        """

        for _ in range(max_pages):
            cards = self.driver.find_elements(*self.PRODUCT_CARD_BY_NAME(product_name))
            if cards:
                return cards[0]

            if not self.has_next_page():
                break

            self.go_to_next_page()

        return None

    def is_product_visible(self, product_name: str) -> bool:
        """
        Checks if a product is visible on the current page only
        (no pagination).
        """
        cards = self.driver.find_elements(*self.PRODUCT_CARD_BY_NAME(product_name))
        return len(cards) > 0


    # Product actions
    def add_product_to_cart(self, product_name: str, quantity: int):
        """Add product to cart with given quantity"""

        product_card = self.find_product_card(product_name)
        assert product_card, f"Product '{product_name}' not found in shop"

        quantity_input = product_card.find_element(*self.QUANTITY_INPUT)
        add_button = product_card.find_element(*self.ADD_TO_CART_BUTTON)

        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        add_button.click()


    # Pagination helpers
    def has_next_page(self) -> bool:
        buttons = self.driver.find_elements(*self.NEXT_PAGE_BUTTON)
        return bool(buttons) and "disabled" not in buttons[0].get_attribute("class")

    def go_to_next_page(self):
        self.click(self.NEXT_PAGE_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))


    # Compliance / Security
    def is_underage_notice_visible(self) -> bool:
        """Check if underage notice is displayed"""
        elements = self.driver.find_elements(*self.UNDERAGE_NOTICE)
        return bool(elements) and elements[0].is_displayed()
