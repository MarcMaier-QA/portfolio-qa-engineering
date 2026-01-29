import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage
from TestAutomation.utils.constants import CHECKOUT_URL


class CheckoutPage(BasePage):
    # Locators
    REMOVE_ICON = (By.CSS_SELECTOR, "a.remove-icon")
    # Die Preise
    PRODUCT_TOTAL = (By.XPATH, "//div[@class='product-total-container']//h5[2]")
    SHIPPING_COST = (By.XPATH, "//div[@class='shipment-container']//h5[2]")
    TOTAL_COST = (By.XPATH, "//div[@class='total-container']//h5[2]")
    # Die Leermeldung
    EMPTY_CART_MESSAGE = (By.XPATH, "//h2[normalize-space()='Your cart is empty']")
    # Der Checkoutknopf
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".headerIcon:nth-of-type(3)")

    def PRODUCT_REMOVE_BUTTON(self, product_name: str):
        """
        Findet das '×' Icon basierend auf dem Produktnamen.
        Struktur: h5 -> hoch zum Hauptcontainer -> runter zum remove-icon
        """
        xpath = (
            f"//div[contains(@class, 'checkout-card-item-container')]"
            f"[.//h5[contains(normalize-space(.), '{product_name}')]]"
            f"//a[@class='remove-icon']"
        )
        return (By.XPATH, xpath) # Gibt einen tuple zurück aus Suchstrategie und Selektor

    def remove_button_for_product(self, product_name: str):
        return (
            By.XPATH,
            f"//h5[text()='{product_name}']"
            "/ancestor::div[contains(@class,'checkout-card-item-container')]"
            "//a[contains(@class,'remove-icon')]"
        )

    # Navigation
    def navigate_to_checkout(self):
        """Navigiert zum Checkout und wartet nur auf die URL."""
        self.open(CHECKOUT_URL)
        # Warte bis die URL stimmt, das ist am sichersten gegen Timeouts
        self.wait.until(EC.url_contains("checkout"))

    def clear_cart_if_not_empty(self):
        """Entfernt zuverlässig alle Produkte aus dem Warenkorb."""
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
        """Entfernt ein spezifisches Produkt aus dem Warenkorb."""
        # 1. Den Locator generieren
        remove_locator = self.PRODUCT_REMOVE_BUTTON(product_name)

        # 2. Das gibt dem Warenkorb die nötige Zeit, um die Äpfel anzuzeigen
        button_element = self.wait.until(
            EC.element_to_be_clickable(remove_locator),
            message=f"Konnte Lösch-Button für '{product_name}' nicht finden. Name prüfen!"
        )

        # 3. Klick ausführen
        self.driver.execute_script("arguments[0].click();", button_element)

        # 4. Warten, bis die Zeile verschwindet (DOM-Update abwarten)
        self.wait.until(EC.staleness_of(button_element))
        return self

    # Get-Methoden für Preise
    def get_shipping_cost(self) -> str:
        """Gibt die angezeigten Versandkosten als String zurück (z.B. '5.00€')"""
        return self.get_text(self.SHIPPING_COST)

    def get_product_total(self) -> str:
        """Gibt die Produkt-Zwischensumme als String zurück"""
        return self.get_text(self.PRODUCT_TOTAL)

    def get_total(self) -> str:
        """Gibt die finale Gesamtsumme als String zurück"""
        return self.get_text(self.TOTAL_COST)

    # Hilfsmethode für Preiskonvertierung
    @staticmethod
    def clean_currency(currency_string: str) -> float:
        """Extrahiert nur die Zahl aus dem String, ignoriert Text wie 'Product Total:'"""
        # Sucht nach Zahlenfolge, die optional ein Komma oder Punkt enthält
        match = re.search(r'(\d+[\.,]\d+)', currency_string)
        if match:
            number_str = match.group(1).replace(',', '.')
            return float(number_str)

        # Fallback für ganze Zahlen (z.B. '5€')
        match_int = re.search(r'(\d+)', currency_string)
        if match_int:
            return float(match_int.group(1))

        raise ValueError(f"Konnte keine Zahl in '{currency_string}' finden")

    def get_shipping_cost_as_float(self) -> float:
        """Gibt die Versandkosten als Float zurück"""
        return self.clean_currency(self.get_shipping_cost())

    def get_product_total_as_float(self) -> float:
        """Gibt die Produkt-Zwischensumme als Float zurück"""
        return self.clean_currency(self.get_product_total())

    def get_total_as_float(self) -> float:
        """Gibt die Gesamtsumme als Float zurück"""
        return self.clean_currency(self.get_total())

    # Warenkorb-Status prüfen
    def is_cart_empty(self) -> bool:
        return bool(
            self.find_elements_no_wait(self.EMPTY_CART_MESSAGE)
        )

    def goto_checkout(self):
        """Klickt auf das Einkaufswagen-Symbol und wartet auf Checkout."""
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.url_contains("checkout"))
        return self

    def verify_shipping_costs(self, expected_shipping: float, expected_subtotal: float):
        """
        Zentrale Hilfsfunktion für Versandkosten-Assertions.

        Prüft:
        1. Zwischensumme (Produktkosten) ist korrekt
        2. Versandkosten sind korrekt
        3. Gesamtsumme (Produkte + Versand) ist korrekt

        Args:
            checkout_page: CheckoutPage Instanz
            expected_shipping: Erwartete Versandkosten
            expected_subtotal: Erwartete Produkt-Zwischensumme
        """
        self.wait.until(
            lambda driver: self.get_product_total_as_float() == expected_subtotal,
            message="Zwischensumme wurde nicht korrekt aktualisiert"
        )

        actual_subtotal = self.get_product_total_as_float()
        actual_shipping = self.get_shipping_cost_as_float()
        actual_total = self.get_total_as_float()

        expected_total = expected_subtotal + expected_shipping

        assert actual_subtotal == expected_subtotal
        assert actual_shipping == expected_shipping
        assert actual_total == expected_total

        return self
