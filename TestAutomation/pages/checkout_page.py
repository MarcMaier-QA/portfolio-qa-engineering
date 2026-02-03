import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage
from TestAutomation.utils.constants import CHECKOUT_URL


class CheckoutPage(BasePage):
    # Locators
    REMOVE_ICON = (By.CSS_SELECTOR, "a.remove-icon")

    # Price elements
    PRODUCT_TOTAL = (By.XPATH, "//div[@class='product-total-container']//h5[2]")
    SHIPPING_COST = (By.XPATH, "//div[@class='shipment-container']//h5[2]")
    TOTAL_COST = (By.XPATH, "//div[@class='total-container']//h5[2]")

    # Empty cart message
    EMPTY_CART_MESSAGE = (By.XPATH, "//h2[normalize-space()='Your cart is empty']")

    # Cart / checkout button in header
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".headerIcon:nth-of-type(3)")

    def PRODUCT_REMOVE_BUTTON(self, product_name: str):
        """
        Builds a dynamic locator for the remove (×) icon based on the product name.

        DOM strategy:
        - Find the checkout card container containing the product name
        - Navigate down to the corresponding remove icon
        """
        xpath = (
            f"//div[contains(@class, 'checkout-card-item-container')]"
            f"[.//h5[contains(normalize-space(.), '{product_name}')]]"
            f"//a[@class='remove-icon']"
        )
        return (By.XPATH, xpath)  # Returns a (By, selector) tuple

    def remove_button_for_product(self, product_name: str):
        """
        Alternative locator strategy for removing a product by name.
        Uses ancestor traversal starting from the product title.
        """
        return (
            By.XPATH,
            f"//h5[text()='{product_name}']"
            "/ancestor::div[contains(@class,'checkout-card-item-container')]"
            "//a[contains(@class,'remove-icon')]"
        )

    # Navigation
    def navigate_to_checkout(self):
        """
        Navigates directly to the checkout page.
        Waits only for the URL to change, which is more stable than waiting for elements.
        """
        self.open(CHECKOUT_URL)
        self.wait.until(EC.url_contains("checkout"))

    def clear_cart_if_not_empty(self):
        """
        Removes all products from the cart if any are present.
        Continues until no remove icons are left in the DOM.
        """
        self.goto_checkout()

        remove_buttons = self.find_elements_no_wait(self.REMOVE_ICON)

        while remove_buttons:
            button = remove_buttons[0]
            button.click()
            self.wait.until(EC.staleness_of(button))
            remove_buttons = self.find_elements_no_wait(self.REMOVE_ICON)

        empty_messages = self.find_elements_no_wait(self.EMPTY_CART_MESSAGE)
        if empty_messages:
            self.wait.until(EC.visibility_of(empty_messages[0]))

        return self

    def remove_product_from_cart(self, product_name: str):
        """
        Removes a specific product from the cart by product name.
        """
        # 1. Build the dynamic locator
        remove_locator = self.PRODUCT_REMOVE_BUTTON(product_name)

        # 2. Wait until the remove button is clickable
        button_element = self.wait.until(
            EC.element_to_be_clickable(remove_locator),
            message=f"Could not find remove button for '{product_name}'. Check product name!"
        )

        # 3. Perform click via JavaScript to avoid overlay/intercept issues
        self.driver.execute_script("arguments[0].click();", button_element)

        # 4. Wait until the cart row is removed from the DOM
        self.wait.until(EC.staleness_of(button_element))
        return self

    # Price getters
    def get_shipping_cost(self) -> str:
        """Returns the displayed shipping cost as a string (e.g. '5.00€')."""
        return self.get_text(self.SHIPPING_COST)

    def get_product_total(self) -> str:
        """Returns the product subtotal as a string."""
        return self.get_text(self.PRODUCT_TOTAL)

    def get_total(self) -> str:
        """Returns the final total price as a string."""
        return self.get_text(self.TOTAL_COST)

    # Helper method for currency conversion
    @staticmethod
    def clean_currency(currency_string: str) -> float:
        """
        Extracts the numeric value from a currency string.
        Ignores labels like 'Product Total:' and handles commas or dots.
        """
        match = re.search(r'(\d+[\.,]\d+)', currency_string)
        if match:
            number_str = match.group(1).replace(',', '.')
            return float(number_str)

        # Fallback for whole numbers (e.g. '5€')
        match_int = re.search(r'(\d+)', currency_string)
        if match_int:
            return float(match_int.group(1))

        raise ValueError(f"Could not extract numeric value from '{currency_string}'")

    def get_shipping_cost_as_float(self) -> float:
        """Returns the shipping cost as a float."""
        return self.clean_currency(self.get_shipping_cost())

    def get_product_total_as_float(self) -> float:
        """Returns the product subtotal as a float."""
        return self.clean_currency(self.get_product_total())

    def get_total_as_float(self) -> float:
        """Returns the total price as a float."""
        return self.clean_currency(self.get_total())

    # Cart state checks
    def is_cart_empty(self) -> bool:
        """Checks whether the cart is empty."""
        return bool(self.find_elements_no_wait(self.EMPTY_CART_MESSAGE))

    def goto_checkout(self):
        """
        Opens the checkout by clicking the cart icon
        and waits until the checkout URL is loaded.
        """
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.url_contains("checkout"))
        return self

    def wait_until_totals_updated(self, expected_subtotal: float):
        """
        Waits until the displayed product subtotal matches the expected value.
        Useful after removing items from the cart.
        """
        self.wait.until(
            lambda driver: self.get_product_total_as_float() == expected_subtotal,
            message="Product subtotal was not updated correctly"
        )

    def get_totals(self) -> dict:
        """
        Returns all relevant checkout totals as a dictionary.
        """
        return {
            "subtotal": self.get_product_total_as_float(),
            "shipping": self.get_shipping_cost_as_float(),
            "total": self.get_total_as_float(),
        }
