from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.pages.base_page import BasePage
from TestAutomation.pages.checkout_page import CheckoutPage


class ShopPage(BasePage):
    # Locators
    # Product cards
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class,'product-card')]")
    PRODUCT_TITLE_IN_CARD = (By.XPATH, ".//p[contains(@class,'lead')]")

    # Product actions
    QUANTITY_INPUT = (By.XPATH, ".//input[@type='number']")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@class,'btn-cart')]")

    # Filters / Notices
    # Typo on GroceryMate is intentional
    ALCOHOL_FILTER = (By.XPATH, "//a[normalize-space()='Alocohol']")
    UNDERAGE_NOTICE = (By.XPATH, "//h2[normalize-space()='Underage Notice']")

    # Pagination
    NEXT_PAGE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'pagination-link') and normalize-space()='Next']"
    )

    # Init / Page lifecycle
    def __init__(self, driver):
        super().__init__(driver)

        self.age_popup = AgeVerificationPopup(self.driver)

    # Navigation
    def go_to_checkout(self) -> CheckoutPage:
        self.click(self.CART_ICON)
        return CheckoutPage(self.driver)

    # Filters / Visibility
    def filter_alcohol(self):
        """Clicks the alcohol filter"""
        self.click(self.ALCOHOL_FILTER)

    def is_underage_notice_visible(self) -> bool:
        """Checks if underage notice is displayed"""
        elements = self.find_elements_no_wait(self.UNDERAGE_NOTICE)
        return bool(elements and elements[0].is_displayed())

    def is_product_visible(self, product_name: str) -> bool:
        """Checks visibility on the CURRENT page only"""
        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        return len(cards) > 0

    # Product actions
    def add_product_to_cart(self, product_name: str, quantity: int):
        product_card = self.find_product_card(product_name)
        if product_card is None:
            return None

        quantity_input = product_card.find_element(*self.QUANTITY_INPUT)
        add_button = product_card.find_element(*self.ADD_TO_CART_BUTTON)

        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        add_button.click()

        return self

    # Product search
    def PRODUCT_CARD_BY_NAME(self, name: str):
        """Dynamic locator for a specific product card"""
        return (
            By.XPATH,
            f"//p[contains(@class,'lead') and contains(normalize-space(), '{name}')]"
            f"/ancestor::div[contains(@class,'product-card')]"
        )

    def find_product_card(self, product_name: str, max_pages: int = 10) -> WebElement | None:
        self._wait_until_product_list_stable()
        return self._find_product_recursive(product_name, 0, max_pages)

    def _find_product_recursive(self, product_name: str, pages_searched: int, max_pages: int) -> WebElement | None:
        if pages_searched >= max_pages:
            return None

        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        if cards:
            return cards[0]

        if not self.has_next_page():
            return None

        self.go_to_next_page()
        return self._find_product_recursive(product_name, pages_searched + 1, max_pages)

    # Pagination helpers
    def has_next_page(self) -> bool:
        buttons = self.find_elements_no_wait(self.NEXT_PAGE_BUTTON)
        if not buttons:
            return False

        return "disabled" not in buttons[0].get_attribute("class")

    def go_to_next_page(self):
        old_cards = self.driver.find_elements(*self.PRODUCT_CARD)

        self.click(self.NEXT_PAGE_BUTTON)

        if old_cards:
            self.wait.until(
                EC.staleness_of(old_cards[0]),
                message="ShopPage: product cards did not refresh"
            )

        self._wait_until_product_list_stable()

    # Internal helpers
    def _wait_until_product_list_stable(self, timeout: int = 10):
        """
        Waits until product titles remain unchanged between DOM refreshes.
        timeout currently controlled by WebDriverWait instance.
        """
        previous_titles = []

        def product_titles_stable(driver):
            cards = driver.find_elements(*self.PRODUCT_CARD)
            titles = [
                card.find_element(*self.PRODUCT_TITLE_IN_CARD).text
                for card in cards
            ]

            nonlocal previous_titles
            if titles and titles == previous_titles:
                return True

            previous_titles = titles
            return False

        self.wait.until(
            product_titles_stable,
            message="ShopPage: product list not stable"
        )

    def wait_until_shop_ready(self):
        """
        Wait until the shop is usable (after age verification).
        """
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD),
            message="ShopPage: product cards not present"
        )
        self._wait_until_product_list_stable()

    def has_visible_products(self) -> bool:
        """checks if product cards are visible."""
        cards = self.find_elements_no_wait(self.PRODUCT_CARD)
        return any(card.is_displayed() for card in cards)