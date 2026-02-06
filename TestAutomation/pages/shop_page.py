from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.pages.base_page import BasePage
from TestAutomation.pages.checkout_page import CheckoutPage
from TestAutomation.pages.product_page import ProductPage


class ShopPage(BasePage):
    # Locators
    # Product cards
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class,'product-card')]")
    PRODUCT_TITLE_IN_CARD = (By.XPATH, ".//p[contains(@class,'lead')]")

    # Product actions inside a card
    QUANTITY_INPUT = (By.XPATH, ".//input[@type='number']")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@class,'btn-cart')]")

    # Filters / notices
    # Typo "Alocohol" exists in the application and is intentionally mirrored here
    ALCOHOL_FILTER = (By.XPATH, "//a[normalize-space()='Alocohol']")
    UNDERAGE_NOTICE = (By.XPATH, "//h2[normalize-space()='Underage Notice']")

    # Pagination
    CART_ICON = (By.CSS_SELECTOR, ".headerIcon:nth-of-type(3)")
    NEXT_PAGE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'pagination-link') and normalize-space()='Next']"
    )

    # Init / Page lifecycle
    def __init__(self, driver):
        super().__init__(driver)

        # Age verification popup is part of the shop flow
        # Initializing it here keeps responsibility close to where it is needed
        self.age_popup = AgeVerificationPopup(self.driver)

    # Navigation
    def go_to_checkout(self) -> CheckoutPage:
        """
        Navigates to the checkout via the cart icon.

        Uses click-based navigation instead of direct URLs
        to stay close to real user behavior.
        """
        self.click(self.CART_ICON)
        return CheckoutPage(self.driver)

    # Filters / Visibility
    def filter_alcohol_as_adult(self):
        """
        Applies the alcohol filter for an adult user and waits until the filtered product list is ready.

        The wait is intentionally placed here because changing the category
        triggers a dynamic UI update (DOM refresh).
        """
        # Triggers UI state change
        self.click(self.ALCOHOL_FILTER)

        # Wait until product cards are present after filtering
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD),
            message="ShopPage: product cards not present after applying alcohol filter"
        )

        # Ensure the product list has fully stabilized
        self._wait_until_product_list_ready()

        return self

    def filter_alcohol_as_underage(self):
        """
        Applies the alcohol filter for an adult user and waits until the filtered product list is ready.

        The wait is intentionally placed here because changing the category
        triggers a dynamic UI update (DOM refresh).
        """
        # Triggers UI state change
        self.click(self.ALCOHOL_FILTER)

        # Wait until product cards are present after filtering
        self.wait.until(
            EC.visibility_of_element_located(self.UNDERAGE_NOTICE),
            message = "ShopPage: underage notice not visible"
        )

    def is_underage_notice_visible(self) -> bool:
        """
        Checks whether the underage notice is currently displayed.

        Uses a no-wait lookup to allow flexible state assertions.
        """
        elements = self.find_elements_no_wait(self.UNDERAGE_NOTICE)
        return bool(elements and elements[0].is_displayed())

    def is_product_visible(self, product_name: str) -> bool:
        """
        Checks whether a product is visible on the CURRENT page only.

        Pagination is intentionally ignored here to allow
        precise assertions in pagination-related tests.
        """
        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        return len(cards) > 0

    # Product actions
    def add_product_to_cart(self, product_name: str, quantity: int):
        """
        Adds a product with the given quantity to the cart.

        Returns self for fluent test chaining.
        """
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
        """
        Dynamic locator for a specific product card by name.

        The locator targets the title first and navigates up
        to the corresponding product card container.
        """
        return (
            By.XPATH,
            f"//p[contains(@class,'lead') and contains(normalize-space(), '{name}')]"
            f"/ancestor::div[contains(@class,'product-card')]"
        )

    def find_product_card(self, product_name: str, max_pages: int = 10) -> WebElement | None:
        """
        Searches for a product card across multiple pages.

        Pagination is handled recursively to keep the logic
        readable and explicit.
        """
        self._wait_until_product_list_ready()
        return self._find_product_recursive(product_name, 0, max_pages)

    def _find_product_recursive(
        self,
        product_name: str,
        pages_searched: int,
        max_pages: int
    ) -> WebElement | None:
        """
        Recursively searches through paginated product lists.

        Stops when:
        - the product is found
        - no next page exists
        - the maximum number of pages is reached
        """
        if pages_searched >= max_pages:
            return None

        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        if cards:
            return cards[0]

        if not self.has_next_page():
            return None

        self.go_to_next_page()
        return self._find_product_recursive(
            product_name,
            pages_searched + 1,
            max_pages
        )

    # Pagination helpers
    def has_next_page(self) -> bool:
        """
        Checks whether the 'Next' pagination button is available and enabled.
        """
        buttons = self.find_elements_no_wait(self.NEXT_PAGE_BUTTON)
        if not buttons:
            return False

        return "disabled" not in buttons[0].get_attribute("class")

    def go_to_next_page(self):
        """
        Navigates to the next pagination page.

        Uses staleness detection to ensure the product list
        was actually refreshed.
        """
        old_cards = self.driver.find_elements(*self.PRODUCT_CARD)

        self.click(self.NEXT_PAGE_BUTTON)

        if old_cards:
            self.wait.until(
                EC.staleness_of(old_cards[0]),
                message="ShopPage: product cards did not refresh"
            )

        self._wait_until_product_list_ready()

    # Internal helpers
    def  _wait_until_product_list_ready(self):
        """
        Waits until the product list is ready for interaction.

        A product list is considered ready when:
        - product cards are present in the DOM
        - at least one product card is visible
        - at least one product card is interactable
        """

        # Wait until product cards exist
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD),
            message="ShopPage: product cards not present"
        )

        # Wait until at least one product card is visible
        self.wait.until(
            EC.visibility_of_any_elements_located(self.PRODUCT_CARD),
            message="ShopPage: product cards not visible"
        )

        # Ensure UI is interactable (first card clickable)
        self.wait.until(
            EC.element_to_be_clickable(self.PRODUCT_CARD),
            message="ShopPage: product cards not clickable"
        )

    def wait_until_shop_ready(self):
        """
        Waits until the shop page is fully usable.

        This is especially important after age verification
        or page transitions.
        """
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_CARD),
            message="ShopPage: product cards not present"
        )
        self._wait_until_product_list_ready()

    def has_visible_products(self) -> bool:
        """
        Checks whether at least one product card is visible.
        """
        cards = self.find_elements_no_wait(self.PRODUCT_CARD)
        return any(card.is_displayed() for card in cards)

    def open_product(self, product_name: str) -> ProductPage:
        """
        Opens the product detail page for the given product.

        Raises an explicit assertion error if the product
        cannot be found in the shop.
        """
        product_card = self.find_product_card(product_name)
        if product_card is None:
            raise AssertionError(f"Product '{product_name}' not found in shop")

        title = product_card.find_element(*self.PRODUCT_TITLE_IN_CARD)

        self.wait.until(
            EC.element_to_be_clickable(title),
            message=f"Product '{product_name}' title not clickable"
        ).click()

        product_page = ProductPage(self.driver)
        product_page.wait_until_loaded()
        return product_page
