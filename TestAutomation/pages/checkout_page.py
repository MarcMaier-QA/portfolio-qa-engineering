from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, CHECKOUT_URL
import time


class CheckoutPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Locators
        self.REMOVE_BUTTON = (By.XPATH, "//a[contains(@href, '/remove')]")
        self.SHIPPING_COST = (By.XPATH, "//div[@class='shipment-container']/h5[contains(@class, 'mb-0')]")
        self.PRODUCT_TOTAL = (By.XPATH, "//div[@class='product-total-container']/h5[contains(@class, 'mb-0')]")
        self.TOTAL_COST = (By.XPATH, "//div[@class='total-container']/h5[contains(@class, 'mb-0')]")
        self.EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(),'Your cart is empty')]")


    # Navigationsmethode
    def navigate_to_checkout(self):
        """Navigiert direkt zur Checkout-Seite."""
        self.driver.get(CHECKOUT_URL)
        # Warten, bis die Seite geladen ist (mindestens ein Container ist sichtbar)
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located(self.TOTAL_COST)
        )


    # Interaktionsmethode (Warenkorb leeren)
    def clear_cart_if_not_empty(self):
        """Leert den Warenkorb zuverlässig (übernimmt die Logik aus dem Helper)."""
        self.navigate_to_checkout()

        # Endlosschleife, bis keine Remove-Buttons mehr gefunden werden
        while True:
            # Suche alle 'Remove'-Buttons
            remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTON)

            if not remove_buttons:
                break  # Warenkorb ist leer

            # Klicke alle gefundenen Buttons (sicherer über JS-Ausführung für schnelle Clicks)
            for btn in remove_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except:
                    continue

            # Kurze Pause für DOM-Aktualisierung
            time.sleep(0.5)

        # Finales Laden des Checkouts zur Bestätigung
        self.navigate_to_checkout()


    # Get-Methoden (für Assertions)
    def get_shipping_cost(self) -> str:
        """Gibt die angezeigten Versandkosten als String zurück (z.B. '$10.00')."""
        return WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.SHIPPING_COST)
        ).text


    def get_product_total(self) -> str:
        """Gibt die angezeigte Produkt-Gesamtsumme als String zurück."""
        return WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.PRODUCT_TOTAL)
        ).text


    def get_total(self) -> str:
        """Gibt die angezeigte finale Gesamtsumme als String zurück."""
        return WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.TOTAL_COST)
        ).text