from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, CHECKOUT_URL
import time


OLD_TOTAL_TC10_STR = "20.00€"


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
        """Navigiert direkt zur Checkout-Seite und wartet auf das Laden der Gesamtsumme."""
        self.driver.get(CHECKOUT_URL)
        # Warten, bis die Seite geladen ist (Total-Container sollte der stabilste sein)
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located(self.TOTAL_COST)
        )

    # Interaktionsmethode (Warenkorb leeren)
    def clear_cart_if_not_empty(self):
        """Leert den Warenkorb zuverlässig (übernimmt die Logik aus dem Helper)."""
        self.navigate_to_checkout()

        # Endlosschleife, bis keine Remove-Buttons mehr gefunden werden
        while True:
            remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTON)

            if not remove_buttons:
                break  # Warenkorb ist leer

            # Klicke alle gefundenen Buttons (sicherer über JS-Ausführung)
            for btn in remove_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except:
                    continue

            # Kurze Pause für DOM-Aktualisierung
            time.sleep(0.5)

        # Finales Laden des Checkouts zur Bestätigung
        self.navigate_to_checkout()

    # Interaktionsmethode (Produkt entfernen)
    def remove_product_from_cart(self, product_name: str):
        """
        Entfernt ein spezifisches Produkt aus dem Warenkorb (wichtig für TC-10).
        """

        # 1. Dynamischer XPATH für den spezifischen Entfernen-Button (a.remove-icon)
        PRODUCT_REMOVE_LOCATOR = (
            By.XPATH,
            # Sucht den Container, der den Produktnamen enthält,
            # und sucht darin nach dem Link mit der Klasse 'remove-icon'.
            f"//div[contains(., '{product_name}')]//a[@class='remove-icon']"
        )

        # 2. Warten und Klicken
        try:
            remove_btn = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.element_to_be_clickable(PRODUCT_REMOVE_LOCATOR)
            )

            remove_btn.click()

            # 3. Warten auf die Aktualisierung des Warenkorbs (WICHTIG für TC-10!)
            # Wir warten, bis der alte Gesamtbetrag (20.00€) verschwunden ist.
            WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until_not(
                # Prüfe, ob der Text des alten Betrags nicht mehr im Gesamtbetrag-Feld vorhanden ist.
                EC.text_to_be_present_in_element(self.TOTAL_COST, OLD_TOTAL_TC10_STR)
            )

        except Exception as e:
            raise Exception(f"Fehler beim Entfernen von '{product_name}' aus dem Warenkorb: {e}")

    # Get-Methoden (für Assertions)
    def get_shipping_cost(self) -> str:
        """Gibt die angezeigten Versandkosten als String zurück (z.B. '5.00€')."""
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